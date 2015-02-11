# Huge thanks to RubyTests( https://github.com/maltize/sublime-text-2-ruby-tests )
import sublime, sublime_plugin
import re
import os
import functools
from glob import glob

class BaseCommand(sublime_plugin.TextCommand):
    def run(self, edit, split_view = False):
        self.load_settings()
        BaseFile.create_base_spec_folder(self.view, self.jasmine_path)
        self.split_view = split_view
        self.defer(lambda: self._run(edit))

    def defer(self, fn):
        sublime.status_message("Jasmine: Indexing")
        self.call(fn) 

    def call(self, fn):
        fn()
        sublime.status_message("Jasmine: Done")

    def load_settings(self):
        settings = sublime.load_settings("Jasmine.sublime-settings")
        self.ignored_directories = settings.get("ignored_directories", [])
        self.jasmine_path = settings.get("jasmine_path", "spec")
        self.spec_file_extension = settings.get("spec_file_extension", ".spec.js")

    def window(self):
        return self.view.window()

class JasmineSwitchCommand(BaseCommand):
    def _run(self, edit):
        file_type = self.file_type()
        if not file_type:
            return

        alternates = self.reduce_alternatives(file_type)
        if alternates:
            self.show_alternatives(alternates)
        else:
            SpecFileInterface(self).interact()

    def reduce_alternatives(self, file_type):
        possible_alternate_files = file_type.possible_alternate_files()
        alternates = self.project_files(lambda file: file in possible_alternate_files)

        self.jasmine_path_in_folder_name = file_type.folder_contains(self.jasmine_path)
        base_path, _ = file_type.split_folder_path_after(self.jasmine_path)

        for alternate in alternates:
            if not self.jasmine_path_in_folder_name:
                base_path, _ = BaseFile.split_after(alternate, self.jasmine_path)

            if self.alternate_exists_in_path(base_path, alternate) or self.file_type_exists_in_path(base_path, file_type):
                alternates = [alternate]
                break

        return alternates

    def alternate_exists_in_path(self, base_path, alternate):
        return self.jasmine_path_in_folder_name and alternate.find(base_path) >= 0

    def file_type_exists_in_path(self, base_path, file_type):
        return not self.jasmine_path_in_folder_name and file_type.folder_name.find(base_path) >= 0

    def show_alternatives(self, alternates):
        if self.split_view:
            ShowPanels(self.window()).split()
        if len(alternates) == 1:
            self.window().open_file(alternates.pop())
        else:
            callback = functools.partial(self.on_selected, alternates)
            self.window().show_quick_panel(alternates, callback)

    def file_type(self):
        file_name = self.view.file_name()
        if JasmineFile.test(file_name):
            return JasmineFile(file_name)
        elif JSFile.test(file_name):
            return JSFile(file_name)

    def on_selected(self, alternates, index):
        if index == -1:
            return
        self.window().open_file(alternates[index])

    def project_files(self, file_matcher):
        directories = self.window().folders()
        return [os.path.join(dirname, file) for directory in directories for dirname, _, files in self.walk(directory) for file in filter(file_matcher, files)]

    def walk(self, directory):
        for dir, dirnames, files in os.walk(directory):
            dirnames[:] = [dirname for dirname in dirnames if dirname not in self.ignored_directories]
            yield dir, dirnames, files

class JasmineCreateSpecCommand(BaseCommand):
    def _run(self, edit):
        SpecFileInterface(self).interact()

class JasmineToggleQuotes(sublime_plugin.TextCommand):
    def run(self, edit):
        active_replacer = SnippetReplacer('.sublime-snippet')
        inactive_replacer = SnippetReplacer('.sublime-snippetx')
        if active_replacer.has_snippets() and inactive_replacer.has_snippets():
            active_replacer.replace()
            inactive_replacer.replace()
            
            sublime.status_message("Jasmine: Making %s active" % inactive_replacer.dirname())
        else:
            sublime.status_message("Jasmine: couldn't find snippets in: %s" % SnippetReplacer.snippets_path())

##
# Classes
##

class ShowPanels():
    def __init__(self, window):
        self.window = window

    def split(self):
        self.window.run_command('set_layout', {
            "cols": [0.0, 0.5, 1.0],
            "rows": [0.0, 1.0],
            "cells": [[0, 0, 1, 1], [1, 0, 2, 1]]
        })
        self.window.focus_group(1)

class BaseFile():
    def __init__(self, file_name):
        self.folder_name, self.file_name = os.path.split(file_name)
        self.absolute_path = file_name

    def parent_dir_name(self):
        head_dir, tail_dir = os.path.split(self.folder_name)
        return tail_dir

    def split_folder_path_after(self, path):
        if self.folder_contains(path):
            return BaseFile.split_after(self.folder_name, path)
        else:
            return (None, None)

    def folder_contains(self, path):
        return self.folder_name.find(path) >= 0

    @classmethod
    def create_base_spec_folder(cls, view, base_spec_path):
        base, _ = os.path.split(view.file_name())
        for folder in view.window().folders():
            spec_path = os.path.join(folder, base_spec_path)
            if base.find(folder) >= 0 and not os.path.exists(spec_path):
                try:
                    os.mkdir(spec_path)
                except FileNotFoundError:
                    sublime.status_message("Jasmine: Error creating the spec folder on %s. Maybe the jasmine_path is missing a folder?" % spec_path)

    @classmethod
    def split_after(cls, base_path, reference_path):
        splitted = base_path.split(reference_path, 1)
        return os.path.split(splitted[1]) if len(splitted) > 1 else (splitted[0], None)


class JSFile(BaseFile):
    def possible_alternate_files(self):
        return [
            self.file_name.replace(".js", "_spec.js"),
            self.file_name.replace(".js", "-spec.js"),
            self.file_name.replace(".js", ".spec.js")
        ]

    @classmethod
    def test(cls, file_name):
        return re.search('\w+\.js', file_name)

class JasmineFile(BaseFile):
    def possible_alternate_files(self):
        possible_set = set([self.file_name.replace("_spec.js", ".js"), self.file_name.replace("-spec.js", ".js"), self.file_name.replace(".spec.js", ".js")])
        file_name_set = set([self.file_name])
        return list(possible_set - file_name_set)

    @classmethod
    def test(cls, file_name):
        return re.search('\w+\.spec.js', file_name) or re.search('\w+\_spec.js', file_name) or re.search('\w+\-spec.js', file_name)

class SpecFileInterface():
    relative_paths = []
    full_torelative_paths = {}
    rel_path_start = 0

    def __init__(self, command):
        self.ignored_directories = command.ignored_directories
        self.jasmine_path = command.jasmine_path
        self.spec_file_extension = command.spec_file_extension
        self.window = command.window()
        self.current_file = command.view.file_name()
        self.split_view = command.split_view

    def interact(self):
        self.build_relative_paths()
        self.window.show_quick_panel(self.relative_paths, self.dir_selected)

    def build_relative_paths(self):
        folders = self.active_project(self.window.folders())
        self.relative_paths = []
        self.full_torelative_paths = {}
        for path in folders:
            rootfolders = os.path.split(path)[-1]
            self.rel_path_start = len(os.path.split(path)[0]) + 1
            self.add_path(rootfolders, path)
            self.walk_dir_paths(path)

    def add_path(self, path_key, path_value):
        if self.is_valid_path(path_key) and self.is_valid_path(path_value):
            self.full_torelative_paths[path_key] = path_value
            self.relative_paths.append(path_key)

    def walk_dir_paths(self, path):
        for base, dirs, files in os.walk(path):
            self.remove_ignored_directories(dirs)
            for dir in dirs:
                dir_path = os.path.join(base, dir)
                relative_path = dir_path[self.rel_path_start:]
                self.add_path(relative_path, dir_path)

    def remove_ignored_directories(self, dirs):
        for ignored_dir in self.ignored_directories:
            if ignored_dir in dirs:
                dirs.remove(ignored_dir)

    def active_project(self, folders):
        result = list(folders)
        for folder in folders:
            project_name = os.path.split(folder)[-1]
            if not re.search(project_name, self.current_file):
                result.remove(folder)
        return result

    def is_valid_path(self, path):
        if not self.current_file.find(self.jasmine_path) >= 0:
            return path.find(self.jasmine_path) >= 0
        return True

    def dir_selected(self, selected_index):
        if selected_index != -1:
            self.selected_dir = self.relative_paths[selected_index]
            self.selected_dir = self.full_torelative_paths[self.selected_dir]
            self.window.show_input_panel("File name", self.suggest_file_name(self.selected_dir), self.file_name_input, None, None)

    def suggest_file_name(self, path):
        current_file = os.path.split(self.current_file)[-1]
        return self.set_file_name(path, current_file)

    def set_file_name(self, path, current_file):
        if self.current_file.find(self.jasmine_path) >= 0:
            return re.sub('.spec.js|_spec.js|-spec.js', '.js', current_file)
        else:
            return current_file.replace('.js', self.spec_file_extension)

    def file_name_input(self, file_name):
        full_path = os.path.join(self.selected_dir, file_name)

        if os.path.lexists(full_path):
            self.window.open_file(full_path)
            return
        else:
            self.create_and_open_file(full_path)

    def create_and_open_file(self, path):
        if not os.path.exists(path):
            self.create_folders(path)

        if self.split_view:
            ShowPanels(self.window).split()

        with open(path, 'w') as f:
            f.write("")

        view = self.window.open_file(path)
        sublime.set_timeout(lambda: view.run_command("insert_snippet", { "name": 'Packages/Jasmine/snippets/describe.sublime-snippet' }), 5)

    def create_folders(self, filename):
        base, filename = os.path.split(filename)
        if not os.path.exists(base):
            parent = os.path.split(base)[0]
            if not os.path.exists(parent):
                self.create_folders(parent)
            os.mkdir(base)

class SnippetReplacer():
    def __init__(self, current):
        token = 'x'
        self.current     = current
        self.replacement = current.replace(token, '') if token in current else current + token
        
        path = os.path.join(SnippetReplacer.snippets_path(), '**', '*' + current)
        self.snippets = glob(path)

    def replace(self):
        for snippet in self.snippets:
            os.rename(snippet, snippet.replace(self.current, self.replacement))

    def dirname(self):
        if self.has_snippets():
            first_snippet = self.snippets[0]
            return os.path.basename(os.path.dirname(first_snippet))
        else:
            return ''

    def has_snippets(self):
        return len(self.snippets) > 0

    @classmethod
    def snippets_path(cls):
        return os.path.join(sublime.packages_path(), 'Jasmine JS', 'snippets')
