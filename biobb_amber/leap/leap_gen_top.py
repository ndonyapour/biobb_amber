#!/usr/bin/env python3

"""Module containing the LeapGenTop class and the command line interface."""
import argparse
from pathlib import PurePath
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_amber.leap.common import check_input_path, check_output_path


class LeapGenTop(BiobbObject):
    """
    | biobb_amber.leap.leap_gen_top LeapGenTop
    | Wrapper of the `AmberTools (AMBER MD Package) leap tool <https://ambermd.org/AmberTools.php>`_ module.
    | Generates a MD topology from a molecule structure using tLeap tool from the AmberTools MD package.

    Args:
        input_pdb_path (str): Input 3D structure PDB file. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/structure.leapin.pdb>`_. Accepted formats: pdb (edam:format_1476).
        input_lib_path (str) (Optional): Input ligand library parameters file. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/ligand.lib>`_. Accepted formats: lib (edam:format_3889), zip (edam:format_3987).
        input_frcmod_path (str) (Optional): Input ligand frcmod parameters file. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/ligand.frcmod>`_. Accepted formats: frcmod (edam:format_3888), zip (edam:format_3987).
        input_params_path (str) (Optional): Additional leap parameter files to load with loadAmberParams Leap command. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/frcmod.ionsdang_spce.txt>`_. Accepted formats: in (edam:format_2330), leapin (edam:format_2330), txt (edam:format_2330), zip (edam:format_3987).
        input_source_path (str) (Optional): Additional leap command files to load with source Leap command. File type: input. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/data/leap/leaprc.water.spce.txt>`_. Accepted formats: in (edam:format_2330), leapin (edam:format_2330), txt (edam:format_2330), zip (edam:format_3987).
        output_pdb_path (str): Output 3D structure PDB file matching the topology file. File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/leap/structure.leap.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_top_path (str): Output topology file (AMBER ParmTop). File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/leap/structure.leap.top>`_. Accepted formats: top (edam:format_3881), parmtop (edam:format_3881), prmtop (edam:format_3881).
        output_crd_path (str): Output coordinates file (AMBER crd). File type: output. `Sample file <https://github.com/bioexcel/biobb_amber/raw/master/biobb_amber/test/reference/leap/structure.leap.crd>`_. Accepted formats: crd  (edam:format_3878), mdcrd (edam:format_3878), inpcrd (edam:format_3878).
        properties (dic - Python dictionary object containing the tool parameters, not input/output files):
            * **forcefield** (*list*) - (["protein.ff14SB","DNA.bsc1","gaff"]) Forcefield to be used for the structure generation. Values: protein.ff14SB, protein.ff19SB, DNA.bsc1, DNA.OL15, RNA.OL3, gaff.
            * **binary_path** (*str*) - ("tleap") Path to the tleap executable binary.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **container_path** (*str*) - (None) Container path definition.
            * **container_image** (*str*) - ('afandiadib/ambertools:serial') Container image definition.
            * **container_volume_path** (*str*) - ('/tmp') Container volume path definition.
            * **container_working_dir** (*str*) - (None) Container working directory definition.
            * **container_user_id** (*str*) - (None) Container user_id definition.
            * **container_shell_path** (*str*) - ('/bin/bash') Path to default shell inside the container.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_amber.leap.leap_gen_top import leap_gen_top
            prop = {
                'forcefield': ['protein.ff14SB']
            }
            leap_gen_top(input_pdb_path='/path/to/structure.pdb',
                          output_pdb_path='/path/to/newStructure.pdb',
                          output_top_path='/path/to/newTopology.top',
                          output_crd_path='/path/to/newCoordinates.crd',
                          properties=prop)

    Info:
        * wrapped_software:
            * name: AmberTools tLeap
            * version: >20.9
            * license: LGPL 2.1
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """

    def __init__(self, input_pdb_path: str, output_pdb_path: str,
                 output_top_path: str, output_crd_path: str,
                 input_lib_path: str = None, input_frcmod_path: str = None,
                 input_params_path: str = None, input_source_path: str = None,
                 properties: dict = None, **kwargs):

        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            'in': {'input_pdb_path': input_pdb_path,
                   'input_lib_path': input_lib_path,
                   'input_frcmod_path': input_frcmod_path,
                   'input_params_path': input_params_path,
                   'input_source_path': input_source_path},
            'out': {'output_pdb_path': output_pdb_path,
                    'output_top_path': output_top_path,
                    'output_crd_path': output_crd_path}
        }

        # # Ligand Parameter lists
        # self.ligands_lib_list = []
        # if input_lib_path:
        #     self.ligands_lib_list.append(input_lib_path)
        #
        # self.ligands_frcmod_list = []
        # if input_frcmod_path:
        #     self.ligands_frcmod_list.append(input_frcmod_path)

        # Properties specific for BB
        self.properties = properties
        self.forcefield = properties.get('forcefield', ["protein.ff14SB", "DNA.bsc1", "gaff"])
        self.binary_path = properties.get('binary_path', 'tleap')

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    def check_data_params(self, out_log, err_log):
        """ Checks input/output paths correctness """

        # Check input(s)
        self.io_dict["in"]["input_pdb_path"] = check_input_path(self.io_dict["in"]["input_pdb_path"], "input_pdb_path", False, out_log, self.__class__.__name__)
        self.io_dict["in"]["input_lib_path"] = check_input_path(self.io_dict["in"]["input_lib_path"], "input_lib_path", True, out_log, self.__class__.__name__)
        self.io_dict["in"]["input_frcmod_path"] = check_input_path(self.io_dict["in"]["input_frcmod_path"], "input_frcmod_path", True, out_log, self.__class__.__name__)
        # self.io_dict["in"]["input_params_path"] = check_input_path(self.io_dict["in"]["input_params_path"], "input_params_path", True, out_log, self.__class__.__name__)
        # self.io_dict["in"]["input_source_path"] = check_input_path(self.io_dict["in"]["input_source_path"], "input_source_path", True, out_log, self.__class__.__name__)

        # Check output(s)
        self.io_dict["out"]["output_pdb_path"] = check_output_path(self.io_dict["out"]["output_pdb_path"], "output_pdb_path", False, out_log, self.__class__.__name__)
        self.io_dict["out"]["output_top_path"] = check_output_path(self.io_dict["out"]["output_top_path"], "output_top_path", False, out_log, self.__class__.__name__)
        self.io_dict["out"]["output_crd_path"] = check_output_path(self.io_dict["out"]["output_crd_path"], "output_crd_path", False, out_log, self.__class__.__name__)

    @launchlogger
    def launch(self):
        """Launches the execution of the LeapGenTop module."""

        # check input/output paths and parameters
        self.check_data_params(self.out_log, self.err_log)

        # Setup Biobb
        if self.check_restart():
            return 0
        self.stage_files()

        # Creating temporary folder & Leap configuration (instructions) file
        if self.container_path:
            instructions_file = str(PurePath(self.stage_io_dict['unique_dir']).joinpath("leap.in"))
            instructions_file_path = str(PurePath(self.container_volume_path).joinpath("leap.in"))
            self.tmp_folder = None
        else:
            self.tmp_folder = fu.create_unique_dir()
            instructions_file = str(PurePath(self.tmp_folder).joinpath("leap.in"))
            fu.log('Creating %s temporary folder' % self.tmp_folder, self.out_log)
            instructions_file_path = instructions_file

        ligands_lib_list = []
        if self.io_dict['in']['input_lib_path'] is not None:
            if self.io_dict['in']['input_lib_path'].endswith('.zip'):
                ligands_lib_list = fu.unzip_list(self.stage_io_dict['in']['input_lib_path'], dest_dir=self.tmp_folder, out_log=self.out_log)
            else:
                ligands_lib_list.append(self.stage_io_dict['in']['input_lib_path'])

        ligands_frcmod_list = []
        if self.io_dict['in']['input_frcmod_path'] is not None:
            if self.io_dict['in']['input_frcmod_path'].endswith('.zip'):
                ligands_frcmod_list = fu.unzip_list(self.stage_io_dict['in']['input_frcmod_path'], dest_dir=self.tmp_folder, out_log=self.out_log)
            else:
                ligands_frcmod_list.append(self.stage_io_dict['in']['input_frcmod_path'])

        amber_params_list = []
        if self.io_dict['in']['input_params_path'] is not None:
            if self.io_dict['in']['input_params_path'].endswith('.zip'):
                amber_params_list = fu.unzip_list(self.stage_io_dict['in']['input_params_path'], dest_dir=self.tmp_folder, out_log=self.out_log)
            else:
                amber_params_list.append(self.stage_io_dict['in']['input_params_path'])

        leap_source_list = []
        if self.io_dict['in']['input_source_path'] is not None:
            if self.io_dict['in']['input_source_path'].endswith('.zip'):
                leap_source_list = fu.unzip_list(self.stage_io_dict['in']['input_source_path'], dest_dir=self.tmp_folder, out_log=self.out_log)
            else:
                leap_source_list.append(self.stage_io_dict['in']['input_source_path'])

        with open(instructions_file, 'w') as leapin:
            # Forcefields loaded by default:
            # Protein: ff14SB (PARM99 + frcmod.ff99SB + frcmod.parmbsc0 + OL3 for RNA)
            # leapin.write("source leaprc.protein.ff14SB \n")
            # DNA: parmBSC1 (ParmBSC1 (ff99 + bsc0 + bsc1) for DNA. Ivani et al. Nature Methods 13: 55, 2016)
            # leapin.write("source leaprc.DNA.bsc1 \n")
            # Ligands: GAFF (General Amber Force field, J. Comput. Chem. 2004 Jul 15;25(9):1157-74)
            # leapin.write("source leaprc.gaff \n")

            # Forcefields loaded from input forcefield property
            for t in self.forcefield:
                leapin.write("source leaprc.{}\n".format(t))

            # Additional Leap commands
            for leap_commands in leap_source_list:
                leapin.write("source " + leap_commands + "\n")

            # Additional Amber parameters
            for amber_params in amber_params_list:
                leapin.write("loadamberparams " + amber_params + "\n")

            # Ions libraries
            leapin.write("loadOff atomic_ions.lib \n")

            # Ligand(s) libraries (if any)
            for amber_lib in ligands_lib_list:
                leapin.write("loadOff " + amber_lib + "\n")
            for amber_frcmod in ligands_frcmod_list:
                leapin.write("loadamberparams " + amber_frcmod + "\n")

            # Loading PDB file
            leapin.write("mol = loadpdb " + self.stage_io_dict['in']['input_pdb_path'] + " \n")

            # Saving output PDB file, coordinates and topology
            leapin.write("savepdb mol " + self.stage_io_dict['out']['output_pdb_path'] + " \n")
            leapin.write("saveAmberParm mol " + self.stage_io_dict['out']['output_top_path'] + " " + self.stage_io_dict['out']['output_crd_path'] + "\n")
            leapin.write("quit \n")

        # Command line
        self.cmd = [self.binary_path,
                    '-f', instructions_file_path
                    ]

        # Run Biobb block
        self.run_biobb()

        # Copy files to host
        self.copy_to_host()

        # remove temporary folder(s)
        self.tmp_files.extend([
            self.stage_io_dict.get("unique_dir"),
            self.tmp_folder,
            "leap.log"
        ])
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return self.return_code


def leap_gen_top(input_pdb_path: str, output_pdb_path: str,
                 output_top_path: str, output_crd_path: str,
                 input_lib_path: str = None, input_frcmod_path: str = None,
                 input_params_path: str = None, input_source_path: str = None,
                 properties: dict = None, **kwargs) -> int:
    """Create :class:`LeapGenTop <leap.leap_gen_top.LeapGenTop>`leap.leap_gen_top.LeapGenTop class and
    execute :meth:`launch() <leap.leap_gen_top.LeapGenTop.launch>` method"""

    return LeapGenTop(input_pdb_path=input_pdb_path,
                      input_lib_path=input_lib_path,
                      input_frcmod_path=input_frcmod_path,
                      input_params_path=input_params_path,
                      input_source_path=input_source_path,
                      output_pdb_path=output_pdb_path,
                      output_top_path=output_top_path,
                      output_crd_path=output_crd_path,
                      properties=properties).launch()


def main():
    parser = argparse.ArgumentParser(description='Generating a MD topology from a molecule structure using tLeap program from AmberTools MD package.', formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    # Specific args
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_pdb_path', required=True, help='Input 3D structure PDB file. Accepted formats: pdb.')
    required_args.add_argument('--input_lib_path', required=False, help='Input ligand library parameters file. Accepted formats: lib, zip.')
    required_args.add_argument('--input_frcmod_path', required=False, help='Input ligand frcmod parameters file. Accepted formats: frcmod, zip.')
    required_args.add_argument('--input_params_path', required=False, help='Additional leap parameter files to load with loadAmberParams Leap command. Accepted formats: leapin, in, txt, zip.')
    required_args.add_argument('--input_source_path', required=False, help='Additional leap command files to load with source Leap command. Accepted formats: leapin, in, txt, zip.')
    required_args.add_argument('--output_pdb_path', required=True, help='Output 3D structure PDB file matching the topology file. Accepted formats: pdb.')
    required_args.add_argument('--output_top_path', required=True, help='Output topology file (AMBER ParmTop). Accepted formats: top.')
    required_args.add_argument('--output_crd_path', required=True, help='Output coordinates file (AMBER crd). Accepted formats: crd.')

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call
    leap_gen_top(input_pdb_path=args.input_pdb_path,
                 input_lib_path=args.input_lib_path,
                 input_frcmod_path=args.input_frcmod_path,
                 input_params_path=args.input_params_path,
                 input_source_path=args.input_source_path,
                 output_pdb_path=args.output_pdb_path,
                 output_top_path=args.output_top_path,
                 output_crd_path=args.output_crd_path,
                 properties=properties)


if __name__ == '__main__':
    main()
