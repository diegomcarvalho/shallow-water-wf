from apps import KFS2d, model_normalize, mpca_ann
import parsl
from parsl.configs.local_threads import config
from parsl.data_provider.files import File

parsl.load(config)

KF = KFS2d("1 10 10 100 10 2 2 0.1 10",
           outputs=[
               parsl.File(
                   "kfs2d_rna_mirror/output/training/qAnalysisExpA.out"),
               parsl.File("kfs2d_rna_mirror/output/training/qModelExpA.out"),
               parsl.File("kfs2d_rna_mirror/output/training/qObservExpA.out")
           ])

KF.result()

MN = model_normalize(
    inputs=[
        KF.outputs[0],
        KF.outputs[1],
        KF.outputs[2]],
    outputs=[
        parsl.File("octave/x.txt"),
        parsl.File("octave/x_gen.txt"),
        parsl.File("octave/x_valid.txt"),
        parsl.File("octave/y.txt"),
        parsl.File("octave/y_gen.txt"),
        parsl.File("octave/y_valid.txt")
    ])

MN.result()

mpca_status = mpca_ann(inputs=MN.outputs, outputs=[
                       parsl.File("mpca-ann/output/ann1.best")])

with open(mpca_status.outputs[0].result(), 'r') as f:
    with open("ann1.best", "w") as w:
        w.write(f.read())
