import os.path
from apps import KFS2d, model_normalize, mpca_ann
import parsl
from parsl.configs.local_threads import config
from parsl.data_provider.files import File

parsl.load(config)

# classes definition
class FileFuture(object):
    '''docstring for FileFuture.'''

    def __init__(self, file_name):
        self._full = os.path.abspath(file_name)
        self._name = os.path.basename(self._full)
        self._path = os.path.dirname(self._full)
        self._future = File(self._full)
        return

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return self._path

    @property
    def path(self):
        return self._path

    @property
    def future(self):
        return self._future


class FileFutureFactory(object):
    '''docstring for FileFutureFactory.'''

    def __init__(self, *argv):
        self._file_list = list()
        for arg in argv:
            self._file_list.append(FileFuture(arg))
        return

    @property
    def file_list(self):
        return self._file_list

    @property
    def future_list(self):
        return [f.future for f in self._file_list]

    def result(self):
        for f in self._file_list:
            f.future.result()
        return


if __name__ == '__main__':

    print("KF Workflow")
    KFS2d_output = FileFutureFactory(
        'kfs2d_rna_mirror/output/training/qAnalysisExpA.out',
        'kfs2d_rna_mirror/output/training/qModelExpA.out',
        'kfs2d_rna_mirror/output/training/qObservExpA.out'
    )

    octave_output = FileFutureFactory(
        'octave/x.txt',
        'octave/x_gen.txt',
        'octave/x_valid.txt',
        'octave/y.txt',
        'octave/y_gen.txt',
        'octave/y_valid.txt',
        'octave/data.txt'
    )

    KF = KFS2d('1 10 10 100 10 2 2 0.1 10', outputs=KFS2d_output.future_list)

    KF.result()

    MN = model_normalize(
        inputs=[x for x in KF.outputs],
        outputs=octave_output.future_list
    )

    MN.result()

    mpca_status = mpca_ann(inputs=MN.outputs, outputs=[
        parsl.File('mpca-ann/output/ann1.best')])

    with open(mpca_status.outputs[0].result(), 'r') as f:
        with open('ann1.best', 'w') as w:
            w.write(f.read())
