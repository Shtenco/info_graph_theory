# Symbolic Axiom System v9

System hash: `200a2f70d658b638ac8da1e9e0262f0b3210709001a6ecf5b5398c1d67cfeff7`

## Status

```text
FORMAL_SYMBOLIC_SYSTEM_VERIFIED
PHYSICAL_TRUTH_NOT_PROVEN_BY_SYMBOLIC_FORM ALONE
CALIBRATION_FORBIDDEN_IN_THEOREM_MODE
```

## Axioms

| Key | Statement | Status |
|:--|:--|:--|
| `A0` | K is the primitive graph/BIP39 arity and K = 6. | `accepted_formal_axiom` |
| `A1` | BIP39 word bits are b = 2K - 1. | `definition` |
| `A2` | BIP39 dictionary size is D = 2^b. | `definition` |
| `A3` | BIP39 phrase length is W = 4K. | `definition` |
| `A4` | BIP39 checksum size is C = K + 2. | `definition` |
| `A5` | BIP39 total phrase bits are T = W b. | `definition` |
| `A6` | The graph sector uses N, p and U = ln(N)/abs(ln(Kp)). | `definition` |
| `A7` | The theorem mode forbids target-specific calibration coefficients. | `rule` |
| `A8` | Fit mode may compute calibration coefficients, but fit mode is not proof mode. | `rule` |

## BIP39 Theorems

| Key | Statement | Derived from | LHS | RHS | Pass |
|:--|:--|:--|--:|--:|:--|
| `T1` | bits_per_word = 2K - 1 | `A0,A1` | `11` | `11` | `True` |
| `T2` | dictionary_size = 2^(2K - 1) | `A0,A1,A2` | `2048` | `2048` | `True` |
| `T3` | words_per_phrase = 4K | `A0,A3` | `24` | `24` | `True` |
| `T4` | sha256_entropy_bits = 4*2^K | `A0` | `256` | `256` | `True` |
| `T5` | checksum_bits = K + 2 | `A0,A4` | `8` | `8` | `True` |
| `T6` | phrase_bits_total = 4K(2K - 1) | `A0,A1,A3,A5` | `264` | `264` | `True` |
| `T7` | table_rows = 4 | `A3` | `4` | `4` | `True` |
| `T8` | table_columns = K | `A0` | `6` | `6` | `True` |

## Frozen Formula Theorems

| Target | Formula | Symbols | Theorem mode | Pass |
|:--|:--|:--|:--|:--|
| `alpha` | `K^-1 * lnDict^-1 * U^-1` | `K, U, lnDict` | `NO_CALIBRATION` | `True` |
| `alpha_s_mZ` | `K^-1 * bits^-1 * bip_density^-1` | `K, bip_density, bits` | `NO_CALIBRATION` | `True` |
| `g_I_squared` | `K * lnDict^-1` | `K, lnDict` | `NO_CALIBRATION` | `True` |
| `infoton_mass_micro_eV` | `m_e[micro-eV] * dict^-2 * entropy^-2 * U` | `U, dict, entropy` | `NO_CALIBRATION` | `True` |
| `proton_mass_MeV` | `m_e * pi * words^2` | `pi, words` | `NO_CALIBRATION` | `True` |
| `W_mass_GeV` | `m_e[GeV] * K * entropy * f1` | `K, entropy, f1` | `NO_CALIBRATION` | `True` |
| `Z_mass_GeV` | `m_e[GeV] * dict * total_bits / U` | `U, dict, total_bits` | `NO_CALIBRATION` | `True` |
| `H_mass_GeV` | `m_e[GeV] * bits^2 * dict` | `bits, dict` | `NO_CALIBRATION` | `True` |
| `sin2_thetaW` | `lnK / checksum` | `checksum, lnK` | `NO_CALIBRATION` | `True` |
| `G_F_GeV_minus2` | `1 / (pi * total_bits * f1)` | `f1, pi, total_bits` | `NO_CALIBRATION` | `True` |
| `Lambda_QCD_GeV` | `U * bip_density / lnK` | `U, bip_density, lnK` | `NO_CALIBRATION` | `True` |

## Numeric Substitution Audit

- `count = 11`
- `pass_readme_style_tolerance = 11/11`
- `mean_relative_error_percent = 0.899025251536`
- `max_relative_error_percent = 1.75723248969`

## Boundary

The symbolic system proves only conditional statements: if the axioms and definitions are accepted, the listed formulas follow inside the formal language.
It does not prove that nature must obey these axioms. That remains an empirical validation problem.
