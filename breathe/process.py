
AUTOCFG_TEMPLATE = r"""
PROJECT_NAME     = "{project_name}"
OUTPUT_DIRECTORY = {output_dir}
GENERATE_LATEX   = NO
GENERATE_MAN     = NO
GENERATE_RTF     = NO
CASE_SENSE_NAMES = NO
INPUT            = {input}
ENABLE_PREPROCESSING = YES
QUIET            = YES
JAVADOC_AUTOBRIEF = YES
JAVADOC_AUTOBRIEF = NO
GENERATE_HTML = NO
GENERATE_XML = YES
ALIASES = "rst=\verbatim embed:rst"
ALIASES += "endrst=\endverbatim"
""".strip()

class DoxygenProcessHandle(object):

    def __init__(self, path_handler, run_process, write_file):

        self.path_handler = path_handler
        self.run_process = run_process
        self.write_file = write_file

    def process(self, project_info, files):

        name = project_info.name()
        cfgfile = "%s.cfg" % name

        full_paths = map(lambda x: project_info.abs_path_to_source_file(x), files)

        cfg = AUTOCFG_TEMPLATE.format(
                project_name=name,
                output_dir=name,
                input=" ".join(full_paths)
                )

        dir_ = "build/breathe/doxygen"
        self.write_file(dir_, cfgfile, cfg)

        self.run_process(['doxygen', cfgfile], cwd=dir_)

        return self.path_handler.join(dir_, name, "xml")

