# Graph Action Optimization v3

Final verdict: `FAIL_BLIND_SCORE: fewer than 6 locked known-blind targets pass`

## Unified Penalized Graph Action

```text
S_total(theta; G, L) = S_U[X; theta] + S_penalty

S_penalty =
  lambda_dof * effective_DOF_ridge(theta)
+ lambda_ridge * ||theta||_2^2
+ lambda_shortcut * I[too few spectral graph invariants are active]
+ lambda_leak * Leakage(theta, locked_known_blind)

Optimization domain:
  train only = {electron, muon, W, Z, H, alpha}

Locked evaluation domain:
  locked_known_blind = {proton, neutron, tau, top, alpha_s, sin2_thetaW, G_F, Planck, Lambda_QCD, Fe56}
```

## Graph Invariants

| Invariant | Value |
|:--|--:|
| `node_count` | `48` |
| `degree_k` | `6` |
| `edge_count` | `143` |
| `trace_laplacian` | `286` |
| `spectral_gap` | `0.409251540621` |
| `lambda_max` | `10.0555675509` |
| `mean_lambda` | `5.95833333333` |
| `heat_t_025` | `0.283519358696` |
| `heat_t_1` | `0.0641824047374` |
| `spectral_entropy` | `3.75189529216` |
| `kirchhoff_log_proxy` | `74.0334169355` |

## Optimized Theta

| Feature | Theta |
|:--|--:|
| `bias` | `-10.1614571324` |
| `gap_x_q_mass` | `-1.72431662598` |
| `entropy_x_generation` | `2.88957669185` |
| `heat_x_spin` | `-2.02901605834` |
| `lambda_max_x_color` | `0` |
| `kirchhoff_x_charge` | `-0.355808862444` |
| `mean_lambda_x_dimensional` | `0` |
| `q_mass` | `1.9300064923` |
| `q_charge_abs` | `-0.0826594244754` |
| `q_spin` | `0.738891739834` |
| `q_generation` | `2.18532984173` |
| `q_color` | `0` |
| `family_mass` | `0.416249627762` |
| `family_coupling` | `-0.416249627762` |
| `family_dimensional` | `0` |

## Penalty Audit

- `train_loss = 0.0768787266575`
- `ridge_norm = 24.9663400627`
- `effective_dof = 4.81495957011`
- `graph_feature_count = 4`
- `penalty_value = 0.39411218773`
- `shortcut_penalty = 0`
- `leakage_penalty = 0`
- `action_value = 0.470990914388`

## Scoreboard

| Model | Split | Pass | Mean log10 error | Max log10 error |
|:--|:--|--:|--:|--:|
| `GRAPH_ACTION_V3` | `train` | 0/6 | `0.219011293901` | `0.516689547319` |
| `GRAPH_ACTION_V3` | `locked_known_blind` | 1/10 | `4.5494765107` | `13.9791811845` |
| `DIMENSIONAL_BASELINE` | `locked_known_blind` | 1/10 | `1.85224794674` | `5.52884718176` |

## Locked Known-Blind Details

| Target | Observed | Predicted | log10 error | Tol | Pass |
|:--|--:|--:|--:|--:|:--|
| `proton_mass_MeV` | `938.2720813` | `6.97119511831` | `2.12902155542` | `0.01` | `False` |
| `neutron_mass_MeV` | `939.5654133` | `35.0239196017` | `1.42856227413` | `0.01` | `False` |
| `tau_mass_MeV` | `1776.86` | `103610.201924` | `1.7657493093` | `0.02` | `False` |
| `top_mass_MeV` | `172690` | `177455.047301` | `0.0118211668631` | `0.03` | `True` |
| `alpha_s_mZ` | `0.1181` | `6843.71046295` | `4.76304172994` | `0.03` | `False` |
| `sin2_thetaW` | `0.223` | `16.86061728` | `1.87856860738` | `0.02` | `False` |
| `G_F_GeV_minus2` | `1.1663787e-05` | `1.5860454783` | `5.13347605602` | `0.05` | `False` |
| `planck_mass_GeV` | `1.22089e+19` | `3.5211647559e+31` | `12.4600098097` | `0.05` | `False` |
| `Lambda_QCD_GeV` | `0.217` | `19.1334439124` | `1.94533341378` | `0.05` | `False` |
| `binding_energy_Fe56_MeV` | `8.79` | `9.22162994832e-14` | `13.9791811845` | `0.02` | `False` |

## Scientific Reading

This v3 layer forces the theory to live inside graph invariants instead of free target-specific constants.
A pass here would still not be a final proof, because locked known-blind data are already historically known.
The future registry is the required next gate: formulas are frozen first, external data arrive later.
