from .exception import BreatheError

from sphinx.application import Sphinx

import os
import fnmatch


from typing import Dict


class ProjectError(BreatheError):
    pass


class NoDefaultProjectError(ProjectError):
    pass


class AutoProjectInfo:
    """Created as a temporary step in the automatic xml generation process"""

    def __init__(self, app: Sphinx, name: str, source_path: str, build_dir: str, reference: str):
        self.app = app

        self._name = name
        self._source_path = source_path
        self._build_dir = build_dir
        self._reference = reference

    def name(self):
        return self._name

    def build_dir(self):
        return self._build_dir

    def abs_path_to_source_file(self, file_):
        """
        Returns full path to the provide file assuming that the provided path is relative to the
        projects conf.py directory as specified in the breathe_projects_source config variable.
        """

        # os.path.join does the appropriate handling if _source_path is an absolute path
        return os.path.join(self.app.confdir, self._source_path, file_)

    def create_project_info(self, project_path):
        """Creates a proper ProjectInfo object based on the information in this AutoProjectInfo"""

        return ProjectInfo(self.app, self._name, project_path, self._source_path, self._reference)


class ProjectInfo:
    def __init__(self, app: Sphinx, name: str, path: str, source_path: str, reference: str):
        self.app = app

        self._name = name
        self._project_path = path
        self._source_path = source_path
        self._reference = reference

    def name(self) -> str:
        return self._name

    def project_path(self):
        return self._project_path

    def source_path(self):
        return self._source_path

    def relative_path_to_xml_file(self, file_):
        """
        Returns relative path from Sphinx documentation top-level source directory to the specified
        file assuming that the specified file is a path relative to the doxygen xml output
        directory.
        """

        # os.path.join does the appropriate handling if _project_path is an absolute path
        full_xml_project_path = os.path.join(self.app.confdir, self._project_path, file_)
        return os.path.relpath(full_xml_project_path, self.app.srcdir)

    def sphinx_abs_path_to_file(self, file_):
        """
        Prepends os.path.sep to the value returned by relative_path_to_file.

        This is to match Sphinx's concept of an absolute path which starts from the top-level source
        directory of the project.
        """
        return os.path.sep + self.relative_path_to_xml_file(file_)

    def reference(self):
        return self._reference

    def domain_for_file(self, file_: str) -> str:
        extension = file_.split(".")[-1]
        try:
            domain = self.app.config.breathe_domain_by_extension[extension]
        except KeyError:
            domain = ""

        domainFromFilePattern = self.app.config.breathe_domain_by_file_pattern
        for pattern, pattern_domain in domainFromFilePattern.items():
            if fnmatch.fnmatch(file_, pattern):
                domain = pattern_domain

        return domain


class ProjectInfoFactory:
    def __init__(self, app: Sphinx):
        self.app = app
        # note: don't access self.app.config now, as we are instantiated at setup-time.

        # Assume general build directory is the doctree directory without the last component.
        # We strip off any trailing slashes so that dirname correctly drops the last part.
        # This can be overridden with the breathe_build_directory config variable
        self._default_build_dir = os.path.dirname(app.doctreedir.rstrip(os.sep))
        self.project_count = 0
        self.project_info_store: Dict[str, ProjectInfo] = {}
        self.project_info_for_auto_store: Dict[str, AutoProjectInfo] = {}
        self.auto_project_info_store: Dict[str, AutoProjectInfo] = {}

    @property
    def build_dir(self) -> str:
        config = self.app.config
        if config.breathe_build_directory:
            return config.breathe_build_directory
        else:
            return self._default_build_dir

    def default_path(self) -> str:
        config = self.app.config
        if not config.breathe_default_project:
            raise NoDefaultProjectError(
                "No breathe_default_project config setting to fall back on "
                "for directive with no 'project' or 'path' specified."
            )

        try:
            return config.breathe_projects[config.breathe_default_project]
        except KeyError:
            raise ProjectError(
                (
                    "breathe_default_project value '%s' does not seem to be a valid key for the "
                    "breathe_projects dictionary"
                )
                % config.breathe_default_project
            )

    def create_project_info(self, options) -> ProjectInfo:
        config = self.app.config
        name = config.breathe_default_project

        if "project" in options:
            try:
                path = config.breathe_projects[options["project"]]
                name = options["project"]
            except KeyError:
                raise ProjectError(
                    "Unable to find project '%s' in breathe_projects dictionary"
                    % options["project"]
                )
        elif "path" in options:
            path = options["path"]
        else:
            path = self.default_path()

        try:
            return self.project_info_store[path]
        except KeyError:
            reference = name
            if not name:
                name = "project%s" % self.project_count
                reference = path
                self.project_count += 1

            project_info = ProjectInfo(self.app, name, path, "NoSourcePath", reference)
            self.project_info_store[path] = project_info
            return project_info

    def store_project_info_for_auto(self, name: str, project_info: AutoProjectInfo) -> None:
        """Stores the project info by name for later extraction by the auto directives.

        Stored separately to the non-auto project info objects as they should never overlap.
        """

        self.project_info_for_auto_store[name] = project_info

    def retrieve_project_info_for_auto(self, options) -> AutoProjectInfo:
        """Retrieves the project info by name for later extraction by the auto directives.

        Looks for the 'project' entry in the options dictionary. This is a less than ideal API but
        it is designed to match the use of 'create_project_info' above for which it makes much more
        sense.
        """

        name = options.get("project", self.app.config.breathe_default_project)
        if name is None:
            raise NoDefaultProjectError(
                "No breathe_default_project config setting to fall back on "
                "for directive with no 'project' or 'path' specified."
            )
        return self.project_info_for_auto_store[name]

    def create_auto_project_info(self, name: str, source_path) -> AutoProjectInfo:
        key = source_path
        try:
            return self.auto_project_info_store[key]
        except KeyError:
            reference = name
            if not name:
                name = "project%s" % self.project_count
                reference = source_path
                self.project_count += 1

            auto_project_info = AutoProjectInfo(
                self.app, name, source_path, self.build_dir, reference
            )
            self.auto_project_info_store[key] = auto_project_info
            return auto_project_info
