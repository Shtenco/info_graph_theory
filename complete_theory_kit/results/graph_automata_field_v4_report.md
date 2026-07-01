# Spectral Graph Automata Field Theory v4

Final verdict: `FAIL_BLIND_SCORE: fewer than 6 locked known-blind targets pass`

## Master Object

```text
U_GNN = (G, L, X_t, A_theta, Phi_theta, R, exp(-sigma n), S_penalty)

X_{t+1} = A(G, L, X_t; automata_basis)
O_k = Phi_theta(pool(X_T, L, heat_kernel))

S_penalty =
  lambda_dof * effective_DOF_ridge(Phi_theta)
+ lambda_ridge * ||theta||_2^2
+ lambda_basis * I[automata basis is not materially used]
+ lambda_leak * Leakage(theta, locked_known_blind)
```

## Automata Basis

| Basis | Role | Update rule |
|:--|:--|:--|
| `identity_memory` | local persistence | `X <- X` |
| `laplacian_diffusion` | spectral locality | `X <- X - eps L X` |
| `neighbor_message` | graph message passing | `X <- D^-1 A X` |
| `phase_rotation` | U(1)-like channel rotation | `X <- R(q_charge) X` |
| `spin_gate` | spin/isospin gate | `X <- tanh(spin * X)` |
| `color_gate` | SU(3)-like color sector proxy | `X <- color-weighted channels` |
| `heat_kernel_gate` | absolute convergence regulator | `X <- exp(-sigma n) X` |
| `spectral_pool` | observable extraction | `pool(X, L, heat kernel)` |

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

## Fit Audit

- `ridge = 0.3`
- `train_loss = 0.221138102785`
- `effective_dof = 3.76296770442`
- `automata_feature_count = 29`
- `penalty_value = 0.75726766162`
- `action_value = 0.978405764406`

## Scoreboard

| Model | Split | Pass | Mean log10 error | Max log10 error |
|:--|:--|--:|--:|--:|
| `SGAFT_V4` | `train` | 0/6 | `0.379306576406` | `0.884982525062` |
| `SGAFT_V4` | `locked_known_blind` | 0/10 | `3.81155196107` | `11.4409539231` |
| `DIMENSIONAL_BASELINE` | `locked_known_blind` | 1/10 | `1.85224794674` | `5.52884718176` |

## Locked Known-Blind Details

| Target | Observed | Predicted | log10 error | Tol | Pass |
|:--|--:|--:|--:|--:|:--|
| `proton_mass_MeV` | `938.2720813` | `32.9018964718` | `1.4551078624` | `0.01` | `False` |
| `neutron_mass_MeV` | `939.5654133` | `159.906801725` | `0.769060084323` | `0.01` | `False` |
| `tau_mass_MeV` | `1776.86` | `38269.296994` | `1.33319727352` | `0.02` | `False` |
| `top_mass_MeV` | `172690` | `65017.1757961` | `0.424239088736` | `0.03` | `False` |
| `alpha_s_mZ` | `0.1181` | `1069.87467987` | `3.95708301182` | `0.03` | `False` |
| `sin2_thetaW` | `0.223` | `7.29806424305` | `1.51490281898` | `0.02` | `False` |
| `G_F_GeV_minus2` | `1.1663787e-05` | `0.996220958727` | `4.93151609417` | `0.05` | `False` |
| `planck_mass_GeV` | `1.22089e+19` | `2.06134144996e+29` | `10.2274733997` | `0.05` | `False` |
| `Lambda_QCD_GeV` | `0.217` | `25.0291319455` | `2.06198605392` | `0.05` | `False` |
| `binding_energy_Fe56_MeV` | `8.79` | `3.18445379603e-11` | `11.4409539231` | `0.02` | `False` |

## Interpretation

This is the graph-neural version of the theory: formulas are not hand-written per target.
The fixed automata basis produces a state, and a penalized readout maps that state to observables.
A negative verdict means the current automata basis is not yet a validated physical theory.
