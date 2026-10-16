# data/: the two public datasets (fetch them yourself)

The trace analyses (`models/trace_profile.py`, `models/figures.py` for Fig. 2, `testbed/x3.py` for the outage
durations) read two public datasets. They are cited, not redistributed here:

| Id | Dataset | License | Commit used |
|---|---|---|---|
| DATA-01 | A. Hassan et al., "Vivisecting Mobility Management in 5G Cellular Networks," ACM SIGCOMM 2022; artifact [SIGCOMM22-5GMobility/artifact](https://github.com/SIGCOMM22-5GMobility/artifact) (U.S. commercial 4G/5G, Minneapolis area) | none stated in the repository | `c612c6fe8ba48edd2038726b47d656266bdb9092` (2022-06-26) |
| DATA-02 | D. Raca et al., "Beyond Throughput, the Next Generation: a 5G Dataset with Channel and Context Metrics," ACM MMSys 2020; [uccmisl/5Gdataset](https://github.com/uccmisl/5Gdataset) (one Irish operator, Cork, static and driving) | GPL-3.0 | `306d92eba81cb4f1195d8b8eba625666a02a10ec` (2020-06-19) |

## Fetch

```bash
cd data
# DATA-01. Two Git-LFS files (table3-system_evaluation/D1.csv, D2.csv; about 640 MB) feed only the authors'
# handover-prediction models and are not needed here, so LFS is skipped.
GIT_LFS_SKIP_SMUDGE=1 git clone https://github.com/SIGCOMM22-5GMobility/artifact sigcomm22-5g-mobility
git -C sigcomm22-5g-mobility checkout c612c6fe8ba48edd2038726b47d656266bdb9092

# DATA-02. The traces are in a zip in the repository root.
git clone https://github.com/uccmisl/5Gdataset ucc-5g-repo
git -C ucc-5g-repo checkout 306d92eba81cb4f1195d8b8eba625666a02a10ec
sha256sum ucc-5g-repo/5G-production-dataset.zip   # abc729d696b5e0ba34a9c6ed35a851f2868d2b5071be5efb8a49691c23bb1a9b (2,177,094 B)
mkdir -p ucc-5g-traces && unzip -q ucc-5g-repo/5G-production-dataset.zip -d ucc-5g-traces -x '__MACOSX/*'
```

The scripts expect these paths:

```
data/sigcomm22-5g-mobility/data/figure9-ho_exec_duration/HO-Duration_Combined.csv   (and the other figure folders)
data/ucc-5g-traces/5G-production-dataset/{Amazon_Prime,Netflix,Download}/{Driving,Static}/*.csv
```
