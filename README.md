# Reproducible analysis development

## How to use the environment Conda file

Install the Conda environment on your machine:

```bash
conda env create -f environment.yml
```

And then activate the environment to use it:

```bash
conda activate <ENV-NAME>
```

If you need to update the environment after editing the yml file:

```bash
conda env update --file environment.yml --prune
```

### Why are there two env files?

Some of the exploratory notebooks use an older version of OSMNX, where a number of functions have since been depreciated. `environment-old.yml` (the `parks-dev-env-old` environment) contains these older libraries, while `environment.yml`  (the `park-safety-env` environment) contains the most up-to-date versions of these packages. `environment.yml`/`park-safety-env` should be used if the safer-parks package is being loaded.

---

## To do

### Organisation

- [X] Record dependencies and make environment file to run notebooks
- [ ] Create Devcontainer file

### Analysis

- [ ] Reproduce current notebooks
- [ ] Add in network analysis