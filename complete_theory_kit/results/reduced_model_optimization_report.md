# Reduced Model Optimization v2 Report

Final verdict: `NOT_PHYSICS_CURRENT_FORM: reduced model still has missing dimensionally complete predictions`

## Optimized Shared Mass Formula

This formula was optimized only on the training masses W, Z, H.
It uses one shared global coefficient and one shared exponent vector.
It is not allowed to use target-specific coefficients such as C_p, C_n, or C_W.

```text
m_e * C_global(190170)
```

- train mean log10 error: `0.0733622829868`
- complexity: `1`
- objective: `0.0833622829868`

## Leaderboard

| Model | Split | Pass | Missing | Mean log10 error | Max log10 error |
|:--|:--|--:|--:|--:|--:|
| `REDUCED_GRAPH_OPTIMIZED_V2` | `train` | 1/4 | 0 | 0.0550324074478 | 0.11004342448 |
| `REDUCED_GRAPH_OPTIMIZED_V2` | `holdout` | 2/10 | 5 | inf | inf |
| `DIMENSIONAL_BASELINE` | `train` | 0/4 | 0 | 1.77487934591 | 2.09760432887 |
| `DIMENSIONAL_BASELINE` | `holdout` | 2/10 | 0 | 0.0991824778833 | 0.348304863048 |
| `RANDOM_LOG_BASELINE` | `train` | 0/4 | 0 | 1.14194400454 | 2.60374254982 |
| `RANDOM_LOG_BASELINE` | `holdout` | 0/10 | 0 | 1.37587045378 | 2.86065124212 |

## Holdout Details

| Model | Target | True | Predicted | log10 error | Tol | Pass | Formula |
|:--|:--|--:|--:|--:|--:|:--|:--|
| `REDUCED_GRAPH_OPTIMIZED_V2` | `proton_mass_MeV` | `938.2720813` | `97176.4219856` | `2.0152321105` | `0.01` | `False` | `m_e * C_global(190170)` |
| `REDUCED_GRAPH_OPTIMIZED_V2` | `neutron_mass_MeV` | `939.5654133` | `97176.4219856` | `2.01463388297` | `0.01` | `False` | `m_e * C_global(190170)` |
| `REDUCED_GRAPH_OPTIMIZED_V2` | `tau_mass_MeV` | `1776.86` | `97176.4219856` | `1.7379076936` | `0.02` | `False` | `m_e * C_global(190170)` |
| `REDUCED_GRAPH_OPTIMIZED_V2` | `alpha_s_mZ` | `0.1181` | `0.113143011172` | `0.0186221648041` | `0.03` | `True` | `pi^3 alpha / 2` |
| `REDUCED_GRAPH_OPTIMIZED_V2` | `sin2_thetaW` | `0.223` | `0.2146` | `0.0166751454182` | `0.02` | `True` | `uncorrected weak proxy` |
| `REDUCED_GRAPH_OPTIMIZED_V2` | `G_F_GeV_minus2` | `1.1663787e-05` | `MISSING` | `inf` | `0.05` | `False` | `MISSING` |
| `REDUCED_GRAPH_OPTIMIZED_V2` | `planck_mass_GeV` | `1.22089e+19` | `MISSING` | `inf` | `0.05` | `False` | `MISSING` |
| `REDUCED_GRAPH_OPTIMIZED_V2` | `cosmological_constant_m_minus2` | `1.089e-52` | `MISSING` | `inf` | `0.2` | `False` | `MISSING` |
| `REDUCED_GRAPH_OPTIMIZED_V2` | `Lambda_QCD_GeV` | `0.217` | `MISSING` | `inf` | `0.05` | `False` | `MISSING` |
| `REDUCED_GRAPH_OPTIMIZED_V2` | `binding_energy_Fe56_MeV` | `8.79` | `MISSING` | `inf` | `0.02` | `False` | `MISSING` |
| `DIMENSIONAL_BASELINE` | `proton_mass_MeV` | `938.2720813` | `1000` | `0.027671206106` | `0.01` | `False` | `category scale` |
| `DIMENSIONAL_BASELINE` | `neutron_mass_MeV` | `939.5654133` | `1000` | `0.0270729785796` | `0.01` | `False` | `category scale` |
| `DIMENSIONAL_BASELINE` | `tau_mass_MeV` | `1776.86` | `1000` | `0.249653210798` | `0.02` | `False` | `category scale` |
| `DIMENSIONAL_BASELINE` | `alpha_s_mZ` | `0.1181` | `0.1` | `0.0722498976135` | `0.03` | `False` | `category scale` |
| `DIMENSIONAL_BASELINE` | `sin2_thetaW` | `0.223` | `0.1` | `0.348304863048` | `0.02` | `False` | `category scale` |
| `DIMENSIONAL_BASELINE` | `G_F_GeV_minus2` | `1.1663787e-05` | `1e-05` | `0.0668395801123` | `0.05` | `False` | `category scale` |
| `DIMENSIONAL_BASELINE` | `planck_mass_GeV` | `1.22089e+19` | `1e+19` | `0.0866765365534` | `0.05` | `False` | `category scale` |
| `DIMENSIONAL_BASELINE` | `cosmological_constant_m_minus2` | `1.089e-52` | `1e-52` | `0.0370278797558` | `0.2` | `True` | `category scale` |
| `DIMENSIONAL_BASELINE` | `Lambda_QCD_GeV` | `0.217` | `0.2` | `0.0354297381845` | `0.05` | `True` | `category scale` |
| `DIMENSIONAL_BASELINE` | `binding_energy_Fe56_MeV` | `8.79` | `8` | `0.0408988880818` | `0.02` | `False` | `category scale` |
| `RANDOM_LOG_BASELINE` | `proton_mass_MeV` | `938.2720813` | `4252.36441971` | `0.656301681781` | `0.01` | `False` | `log-uniform +/-3 decades` |
| `RANDOM_LOG_BASELINE` | `neutron_mass_MeV` | `939.5654133` | `1263.10411779` | `0.128512129546` | `0.01` | `False` | `log-uniform +/-3 decades` |
| `RANDOM_LOG_BASELINE` | `tau_mass_MeV` | `1776.86` | `863.703063828` | `0.313288750617` | `0.02` | `False` | `log-uniform +/-3 decades` |
| `RANDOM_LOG_BASELINE` | `alpha_s_mZ` | `0.1181` | `85.684277633` | `2.86065124212` | `0.03` | `False` | `log-uniform +/-3 decades` |
| `RANDOM_LOG_BASELINE` | `sin2_thetaW` | `0.223` | `1.16980401495` | `0.719808244547` | `0.02` | `False` | `log-uniform +/-3 decades` |
| `RANDOM_LOG_BASELINE` | `G_F_GeV_minus2` | `1.1663787e-05` | `0.000560278602505` | `1.68156445661` | `0.05` | `False` | `log-uniform +/-3 decades` |
| `RANDOM_LOG_BASELINE` | `planck_mass_GeV` | `1.22089e+19` | `8.75061464549e+17` | `1.1446379775` | `0.05` | `False` | `log-uniform +/-3 decades` |
| `RANDOM_LOG_BASELINE` | `cosmological_constant_m_minus2` | `1.089e-52` | `3.95005829046e-51` | `1.55957562474` | `0.2` | `False` | `log-uniform +/-3 decades` |
| `RANDOM_LOG_BASELINE` | `Lambda_QCD_GeV` | `0.217` | `0.000518028390317` | `2.62210617213` | `0.05` | `False` | `log-uniform +/-3 decades` |
| `RANDOM_LOG_BASELINE` | `binding_energy_Fe56_MeV` | `8.79` | `1038.11898464` | `2.07225825822` | `0.02` | `False` | `log-uniform +/-3 decades` |

## Interpretation

The optimization produced a reduced model, but it still cannot be called physics unless it beats baselines on holdout and then survives true future blind tests.
Known holdout is useful for debugging; it is not the same as a real blind prediction.
