from biobb_common.tools import test_fixtures as fx
from biobb_amber.process.process_mdout import ProcessMDOut

class TestProcessMDOut():
    def setUp(self):
        fx.test_setup(self, 'process_mdout')

    def tearDown(self):
        fx.test_teardown(self)
        pass

    def test_ProcessMDOut(self):
        returncode= ProcessMDOut(properties=self.properties, **self.paths).launch()
        assert fx.not_empty(self.paths['output_dat_path'])
        assert fx.equal(self.paths['output_dat_path'], self.paths['ref_output_dat_path'])
        assert fx.exe_success(returncode)