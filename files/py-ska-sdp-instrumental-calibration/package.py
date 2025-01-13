from spack.package import *


class PySkaSdpInstrumentalCalibration(PythonPackage):
    """Batch instrumental calibration pipelines for the SKA SDP. 
    This project contains the functions and scripts needed to generate the initial calibration 
    products during standard SKA batch processing. It includes processing functions to prepare, 
    model and calibrate a visibility dataset, data handling functions for parallel processing, 
    and high level pipeline scripts and notebooks."""

    homepage = "https://gitlab.com/ska-telescope/sdp/science-pipeline-workflows/ska-sdp-instrumental-calibration"
    url = "https://gitlab.com/ska-telescope/sdp/science-pipeline-workflows/ska-sdp-instrumental-calibration/-/archive/0.1.3/ska-sdp-instrumental-calibration-0.1.3.tar.gz"
    git = "https://gitlab.com/ska-telescope/sdp/science-pipeline-workflows/ska-sdp-instrumental-calibration"

    maintainers("saliei")

    license("BSD 3-Clause")

    version("develop-0.1.3", branch="main", preferred=True)
    version("0.1.3", sha256="ede63387b01aa0f50068ebefc9663dcb6e831eac3aa7b8b8372e0e0d97de74a8")
    version("0.1.2", sha256="3f6c49fbed1d4df933b6f4a06ad8dd558619ffadfbbc18d828620f671cd3fbd5")
    version("0.1.1", sha256="401134881d027c01afb3675432fae881421663790579c96651e276d79acffaeb")

    depends_on("python@3.10:", type=("build", "run"))
    depends_on("py-poetry", type="build")
    depends_on("py-poetry-core", type="build")

    depends_on("py-astropy@6.1.0:", type=("build", "run"))
    depends_on("py-distributed@2024.7.1:", type=("build", "run"))
    depends_on("everybeam@0.6.1:", type=("build", "run"))
    depends_on("py-nbmake@1.4.1:", type=("build", "run"))
    depends_on("py-nbqa@1.6.3:", type=("build", "run"))
    depends_on("py-numpy@1.25.4:", type=("build", "run"))
    depends_on("py-jsonschema@4.10.0:", type=("build", "run"))
    depends_on("py-matplotlib@3.9.1:", type=("build", "run"))
    depends_on("py-recommonmark@0.6.0:", type=("build", "run"))
    depends_on("py-xarray@2024.7.0:", type=("build", "run"))
    depends_on("py-isort@5.6.4:", type="build")
    depends_on("py-flake8@6.1.0:", type="build")
    depends_on("py-black@22.3.0:", type="build")
    depends_on("py-setuptools-scm@7.1.0:", type="build")
    depends_on("py-pytest-cov@4.0.0:", type="build")
    depends_on("py-pylint@2.16.2:", type="build")

    # Development dependencies - only if dev variant is enabled
    variant("dev", default=False, description="Install development dependencies")
    depends_on("py-docutils@0.18.0:", type=("build", "run"), when="+dev")
    depends_on("py-markupsafe@0.21.2:", type=("build", "run"), when="+dev")
    depends_on("py-pygments@2.15.1:", type=("build", "run"), when="+dev")
    depends_on("py-pytest@7.4.4:", type=("build", "run"), when="+dev")
    depends_on("py-pytest-pylint@0.21.0:", type=("build", "run"), when="+dev")
    depends_on("py-python-dotenv@0.5.1:", type=("build", "run"), when="+dev")
    depends_on("py-setuptools@62.3.2:", type=("build", "run"), when="+dev")
    depends_on("py-pipdeptree@2.10.2:", type=("build", "run"), when="+dev")

    variant("docs", default=False, description="Install documentation dependencies")
    depends_on("py-sphinx", type=("build", "run"), when="+docs")
    depends_on("py-sphinx-rtd-theme", type=("build", "run"), when="+docs")
    depends_on("py-sphinxcontrib-websupport", type=("build", "run"), when="+docs")

    def setup_build_environment(self, env):
        env.set("POETRY_SOURCE_AUTH_SKAO", '')
        env.set("POETRY_REPOSITORIES_SKAO_URL", "https://artefact.skao.int/repository/pypi-internal/simple")

    def install(self, spec, prefix):
        poetry = which("poetry")
        poetry("config", "virtualenvs.create", "false")
        poetry("install", "--no-dev", "--no-interaction")
        
        if "+dev" in spec:
            poetry("install", "--with", "dev", "--no-interaction")
        if "+docs" in spec:
            poetry("install", "--with", "docs", "--no-interaction")
        
        super().install(spec, prefix)

    def build_args(self, spec, prefix):
        return ["--no-deps"]

    @property
    @llnl.util.lang.memoized
    def _output_version(self):
        spec_vers_str = str(self.spec.version.up_to(3))
        if "develop" in spec_vers_str:
            # Remove 'develop-' from the version in spack
            spec_vers_str = spec_vers_str.partition('-')[2]
        return spec_vers_str

