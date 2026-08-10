# trading-signal

> **⚠️ SUPERSEDED — this repository is legacy and no longer maintained (last substantive commit: 2025-02-13).**
>
> Training-label generation now lives in [harveybc/feature-eng](https://github.com/harveybc/feature-eng), whose `oracle_labels` and `direction_labels` plugins cover and extend this repository's role.
>
> Use feature-eng for any new work. This repository is retained for historical reference only, has no known consumers, and is not required by any current deployment.

## What this was

A small command-line tool that generated training signals (labels) from time-series CSV data by extracting a target column and shifting it forward by a configurable time horizon. It used a plugin architecture via the `trading_signal.plugins` entry-point group and installed a `trading_signal` console script (see [`setup.py`](setup.py)).

Two plugins are registered:

- `default` ([`app/plugins/plugin_default.py`](app/plugins/plugin_default.py)) — builds hourly and daily shifted-target prediction columns from a target column (e.g. `CLOSE`), keeping `DATE_TIME` plus prediction columns.
- `ls` ([`app/plugins/plugin_ls.py`](app/plugins/plugin_ls.py)) — a dataset-preprocessing variant adding rolling standard deviations and column organization intended for NEAT agent training.

## Historical inaccuracies worth knowing

- Earlier versions of this README were titled "Training-Signal" (the repository is `trading-signal`; the installed package is `trading_signal`).
- The old README claimed the default plugin was "the only available plugin", but the `ls` plugin has been registered in `setup.py` alongside it.

## Historical usage — unverified in current environments

The commands below reflect how the tool was originally used. They have **not** been re-verified in current environments.

```bash
git clone https://github.com/harveybc/trading-signal.git
cd trading-signal
pip install -r requirements.txt   # historical — unverified in current environments
pip install .
trading_signal --plugin default --target_column CLOSE --time_horizon 5 \
  --input_file data/input.csv --output_file data/training_signal.csv   # historical — unverified in current environments
```

## Limitations

- No maintenance, no issue support, no compatibility work is planned.
- Committed run residue (`config_out.json`, `debug_out.json`) reflects an old local run, not reference output.
- Remote tests historically depended on an external `data-logger` instance and are unverified.

## License and authors

MIT — see [LICENSE.txt](LICENSE.txt). Contributors are listed in [AUTHORS.rst](AUTHORS.rst).
