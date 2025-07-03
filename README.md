# Reproducible analysis development

## How to use the environment Conda file

Install the Conda environment on your machine:

```bash
conda env create -f environment.yml
```

And then activate the environment to use it:

```bash
conda activate parks-dev-env
```

If you need to update the environment after editing the yml file:

```bash
conda env update --file environment.yml --prune
```

---

## To do

### Organisation

- [X] Record dependencies and make environment file to run notebooks
- [ ] Create Devcontainer file

### Analysis

- [ ] Reproduce current notebooks
- [ ] Add in network analysis