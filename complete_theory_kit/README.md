# Complete Theory Kit

Полный вычислительный комплект для проверки SHTENCO Information Graph Theory  
Дата: 2026-06-30  
Статус: автономный Python-аудит, оптимизация урезанной модели и blind-prediction scaffold без внешних зависимостей

---

## 0. Назначение комплекта

Этот каталог содержит исполняемый проверочный слой для теории информационного графа. Его задача не в том, чтобы заменить математическое доказательство, а в том, чтобы каждое важное численное утверждение можно было повторить одной командой.

Комплект проверяет:

- базовые параметры графа;
- структурные функции;
- исправленные формулы массового сектора;
- BIP39-сектор;
- абсолютную сходимость модельного ряда;
- спектр конечного графового лапласиана;
- таблицу ошибок из большого README;
- корректность генерации машинно-читаемого JSON и CSV.
- оптимизированную урезанную модель без target-specific коэффициентов;
- known-holdout scorecard против baseline-моделей;
- frozen registry для будущих настоящих blind predictions.
- большую ОТО-подобную вариационную формулу `unified_action_v3.py`;
- явный счетчик степеней свободы и штрафуемых параметров.

Главный принцип:

```text
\boxed{
\text{нет проверки}
\Rightarrow
\text{нет численного утверждения}.
}
```

---

## 1. Быстрый запуск

Из PowerShell:

```powershell
cd C:\Users\user\Desktop\THEORY\complete_theory_kit
python run_full_simulation.py
```

Полный v2-запуск:

```powershell
cd C:\Users\user\Desktop\info_graph_theory\complete_theory_kit
python run_complete_v2.py
```

Ожидаемый результат:

```text
FULL THEORY KIT: OK
Report: C:\Users\user\Desktop\THEORY\complete_theory_kit\results\full_theory_report.md
JSON:   C:\Users\user\Desktop\THEORY\complete_theory_kit\results\full_theory_results.json
CSV:    C:\Users\user\Desktop\THEORY\complete_theory_kit\results\convergence.csv
CSV:    C:\Users\user\Desktop\THEORY\complete_theory_kit\results\finite_graph_spectrum.csv
```

Проверка синтаксиса:

```powershell
python -m py_compile C:\Users\user\Desktop\THEORY\complete_theory_kit\run_full_simulation.py
```

---

## 2. Файлы

```text
complete_theory_kit\
├── README.md
├── optimize_reduced_model_v2.py
├── run_complete_v2.py
├── run_full_simulation.py
├── unified_action_v3.py
└── results\
    ├── full_theory_report.md
    ├── full_theory_results.json
    ├── convergence.csv
    ├── finite_graph_spectrum.csv
    ├── reduced_model_optimization_report.md
    ├── reduced_model_optimization.json
    ├── reduced_model_predictions.csv
    ├── frozen_blind_predictions_v2.csv
    ├── unified_action_v3_report.md
    └── unified_action_v3.json
```

Назначение:

| Файл | Назначение |
|:--|:--|
| `run_full_simulation.py` | главный исполняемый аудит |
| `optimize_reduced_model_v2.py` | оптимизация урезанной анти-overfitting модели |
| `run_complete_v2.py` | полный запуск v2 |
| `unified_action_v3.py` | большая ОТО-подобная вариационная формула с DOF-счетчиком |
| `results/full_theory_report.md` | человекочитаемый отчет |
| `results/full_theory_results.json` | полное дерево данных |
| `results/convergence.csv` | контроль сходимости |
| `results/finite_graph_spectrum.csv` | собственные значения конечного лапласиана |
| `results/reduced_model_optimization_report.md` | отчет оптимизации урезанной модели |
| `results/frozen_blind_predictions_v2.csv` | реестр будущих blind predictions |

---

## 3. Архитектура скрипта

Скрипт разбит на смысловые блоки:

| Блок | Функция |
|:--|:--|
| параметры | `TheoryParameters` |
| структурные функции | `structural_functions` |
| физические проверки | `compute_headline_constants` |
| BIP39 | `bip39_checks` |
| сходимость | `convergence_series` |
| граф | `build_small_world_graph` |
| лапласиан | `laplacian_from_adjacency` |
| спектр | `jacobi_eigenvalues_symmetric` |
| аудит README | `extract_readme_error_table` |
| отчеты | `write_report`, `write_csv` |

Главная точка входа:

```python
if __name__ == "__main__":
    main()
```

---

## 4. Базовая теория, которую проверяет код

Граф:

```text
\mathcal G=G(N,K,p).
```

Параметры:

```text
K=6,\qquad
p=4.8027\cdot10^{-42},\qquad
N=4.197668\cdot10^{121}.
```

Структурные функции:

```text
f_2=\ln K,
\qquad
f_3=\sqrt{Kp},
\qquad
f_4=\frac1p,
\qquad
f_5=\frac K{\ln K}.
```

Проверяемое тождество:

```text
\boxed{f_2f_5=K.}
```

---

## 5. Исправленный массовый сектор

### 5.1 Инфотон

Инвариант:

```text
\chi_I=2K^2+2K+1.
```

При `K=6`:

```text
\chi_I=85.
```

Формула:

```text
M_{Inf}
=
\frac{\chi_I m_e}{Kf_1^6}.
```

Python-результат:

```text
5.60058744215 micro-eV
```

### 5.2 Единая константа связи

Формула:

```text
g_I^2
=
2\pi\alpha\frac{f_1}{K}.
```

Python-результат:

```text
0.797650077694
```

### 5.3 Протон

Нормировка:

```text
C_p=0.933250.
```

Формула:

```text
M_p=m_eC_p\pi Kf_1.
```

Python-результат:

```text
938.19866987 MeV
```

### 5.4 W-бозон

Нормировка:

```text
C_W=0.982539.
```

Формула:

```text
M_W=m_eC_Wf_1^2K\sqrt K.
```

Python-результат:

```text
80.3800085651 GeV
```

---

## 6. Таблица ключевых результатов

Актуальный прогон:

| Проверка | Расчет | Референс | Ошибка |
|:--|--:|--:|--:|
| `\alpha` | `0.00729807144137` | `0.00729735256928` | `0.00985114%` |
| `\alpha_s` | `0.113143011172` | `0.118` | `4.11609%` |
| `g_I^2` | `0.797650077694` | `0.801` | `0.418218%` |
| `G` | `6.67635660009e-11` | `6.674e-11` | `0.0353102%` |
| `M_{Inf}` | `5.60058744215 μeV` | `5.60 μeV` | `0.01049%` |
| `M_p` | `938.19866987 MeV` | `938.3 MeV` | `0.0107993%` |
| `M_W` | `80.3800085651 GeV` | `80.38 GeV` | `0.0000107%` |

---

## 7. Абсолютная сходимость

Скрипт проверяет модельный ряд:

```text
\sum_{n=0}^{\infty}(1+n)^qe^{-\sigma n}.
```

В демонстрации:

```text
q=6,
\qquad
\sigma=0.05.
```

Логика:

1. Частичная сумма должна стабилизироваться.
2. Последний член должен стать малым.
3. Верхняя оценка хвоста должна стремиться к нулю.

Результат:

| Величина | Значение |
|:--|--:|
| последняя частичная сумма | `968851442420` |
| последний член | `4.175616946471e-87` |
| верхняя оценка хвоста | `1.693241917442e-85` |

Математический смысл:

```text
\forall q\ge0,\ \forall\sigma>0:
\sum_{n=0}^{\infty}(1+n)^qe^{-\sigma n}<\infty.
```

---

## 8. Конечная графовая симуляция

Скрипт строит небольшой граф малого мира:

| Параметр | Значение |
|:--|--:|
| узлов | `48` |
| локальная связность | `6` |
| демонстрационная вероятность переподключения | `0.08` |
| ребер | `143` |

Далее строится лапласиан:

```text
L=D-W.
```

Проверка спектра:

| Проверка | Значение |
|:--|--:|
| `\mathrm{tr}(L)` | `286` |
| `\sum_i\lambda_i` | `286` |
| ошибка следа | `0` |
| нулевых мод | `1` |
| минимальная положительная мода | `0.409251540621` |
| максимальная мода | `10.0555675509` |

Ключевая идентичность:

```text
\mathrm{tr}(L)=\sum_i\lambda_i.
```

---

## 9. BIP39-сектор

Проверки:

| Параметр | Формула | Значение |
|:--|:--|--:|
| бит на слово | `2K-1` | `11` |
| размер словаря | `2^{2K-1}` | `2048` |
| слов на фразу | `4K` | `24` |
| энтропия SHA-256 | `4\cdot2^K` | `256` |
| контрольная сумма | `K+2` | `8` |
| всего бит | `4K(2K-1)` | `264` |
| строк таблицы | `4` | `4` |
| столбцов таблицы | `K` | `6` |

Итог:

```text
\boxed{8/8=100\%.}
```

---

## 10. JSON-структура

Файл:

```text
results/full_theory_results.json
```

Основные ключи:

```json
{
  "parameters": {},
  "structural_functions": {},
  "headline_constants": [],
  "bip39": [],
  "convergence": [],
  "finite_graph": {},
  "readme_table_audit": {}
}
```

Смысл:

| Ключ | Содержимое |
|:--|:--|
| `parameters` | `K`, `p`, `N`, `f1_working`, `electron_mev` |
| `structural_functions` | `U`, `f1`, `f2`, `f3`, `f4`, `f5`, `f6` |
| `headline_constants` | главные физические проверки |
| `bip39` | дискретный сектор |
| `convergence` | контрольные точки ряда |
| `finite_graph` | спектральные данные графа |
| `readme_table_audit` | статистика таблицы README |

---

## 11. CSV-файлы

### `convergence.csv`

Колонки:

| Колонка | Значение |
|:--|:--|
| `n` | номер контрольной точки |
| `partial_sum` | частичная сумма |
| `last_term` | последний член |
| `tail_bound` | верхняя оценка хвоста |

### `finite_graph_spectrum.csv`

Колонки:

| Колонка | Значение |
|:--|:--|
| `index` | номер собственного значения |
| `lambda` | собственное значение лапласиана |

---

## 12. Что считается PASS

Минимальные условия успешного запуска:

1. Скрипт завершается без исключения.
2. Создаются все четыре результата.
3. Выполняется тождество `f2*f5=K`.
4. Сходимость имеет исчезающий хвост.
5. Графовый спектр неотрицателен.
6. След лапласиана равен сумме собственных значений.
7. BIP39-сектор дает точные значения.
8. Исправленные формулы массового сектора воспроизводят таблицу.

---

## 13. Что этот комплект не доказывает

Комплект не доказывает:

- окончательную физическую истинность теории;
- экспериментальную истинность всех предсказаний;
- вывод нормировок `C_p` и `C_W` из первых принципов;
- безопасность или реализуемость каких-либо устройств;
- лабораторную применимость LENR-модуля.

Он доказывает другое:

```text
\boxed{
\text{численные утверждения текущей версии можно воспроизвести и проверить}.
}
```

---

## 14. Следующее расширение комплекта

План развития:

1. Добавить автоматический парсер формул из Markdown.
2. Проверять все таблицы, а не только выбранные формулы.
3. Создать отдельный `cold_fusion_audit.py`.
4. Вынести параметры в `theory_config.json`.
5. Добавить тесты `unittest`.
6. Добавить строгие PASS/FAIL-коды выхода.
7. Добавить сравнение нескольких версий README.

---

## 14.1 Anti-overfitting v2

Новый слой `optimize_reduced_model_v2.py` пытается сделать то, чего не хватало исходной теории:

1. Запрещает target-specific коэффициенты вроде `C_p`, `C_n`, `C_W`.
2. Оптимизирует одну общую массовую формулу только на train-set.
3. Проверяет known-holdout отдельно.
4. Сравнивает с `DIMENSIONAL_BASELINE` и `RANDOM_LOG_BASELINE`.
5. Считает log-error, чтобы космологические масштабы не взрывали MAE.
6. Выпускает `frozen_blind_predictions_v2.csv`.

Ключевая честность:

```text
known-holdout != true blind prediction
```

Настоящий blind-test возможен только после фиксации формулы до появления или выбора внешнего набора данных.

Ожидаемый результат не обязан быть PASS. Если урезанная модель не проходит, комплект должен сказать это прямо.

---

## 14.2 Unified Action v3

Файл `unified_action_v3.py` создает большую единую формулу в стиле действия ОТО:

```text
S_U[X;theta]
=
S_graph
+S_spec
+S_gauge
+S_matter
+S_mass
+S_mix
+S_reg
+S_obs
+S_penalty
```

В отличие от старых точечных формул, это не одна численная подгонка, а вариационный контейнер с большим числом степеней свободы:

- эффективная графовая метрика;
- лапласиан и графовая связность;
- спектральная плотность;
- U(1), SU(2), SU(3)-подобные секторные поля;
- скалярный сектор;
- фермионный мультиплет;
- массовая карта;
- регуляризатор сходимости;
- наблюдательный functional;
- штраф за DOF, fitted constants и leakage.

Отчет:

```text
results/unified_action_v3_report.md
```

JSON-спецификация:

```text
results/unified_action_v3.json
```

Важно: большая формула сама по себе не доказывает физику. Она только создает правильную форму, в которой можно честно оптимизировать, штрафовать сложность и делать blind predictions.

---

## 15. Финальная схема

```text
README / теория
        |
        v
run_full_simulation.py
        |
        +--> full_theory_report.md
        +--> full_theory_results.json
        +--> convergence.csv
        +--> finite_graph_spectrum.csv
```

Формально:

```text
\boxed{
\text{Theory Text}
\xrightarrow{\text{Python Audit}}
\text{Reproducible Numerical Evidence}
}
```

И главный принцип:

```text
\boxed{
\text{каждая большая формула должна иметь маленький исполняемый тест}.
}
```
---

## Graph Action v3: жесткая графовая оптимизация

Добавлен слой `optimize_graph_action_v3.py`. Его задача - подвести большую формулу не под свободную подгонку, а именно под теорию графов:

```text
S_total(theta; G, L) = S_U[X; theta] + S_penalty
```

где `G` - конечный K=6 граф, `L` - лапласиан, а признаки модели строятся из спектральных инвариантов:

```text
spectral_gap, lambda_max, heat_kernel, spectral_entropy, kirchhoff_log_proxy.
```

Чтобы граф не был декоративным, v3 использует не свободные константы для каждой цели, а фиксированные взаимодействия:

```text
spectral_gap x q_mass
spectral_entropy x generation
heat_kernel x spin
lambda_max x color
kirchhoff_log_proxy x charge
mean_lambda x dimensional_sector
```

Штраф:

```text
S_penalty =
lambda_dof * effective_DOF_ridge(theta)
+ lambda_ridge * ||theta||_2^2
+ lambda_shortcut * I[too few spectral graph interactions are active]
+ lambda_leak * Leakage(theta, locked_known_blind)
```

Текущий машинный результат:

```text
FAIL_BLIND_SCORE: fewer than 6 locked known-blind targets pass
effective_dof = 4.81495957011
graph_feature_count = 4
locked_known_blind = 1/10
```

Это означает: action теперь действительно графовый и проходит барьер сложности `effective_dof < train_count`, но физическую проверку не проходит. Это честная граница текущей версии, а не ошибка скрипта.

Файлы результата:

```text
results/graph_action_v3_report.md
results/graph_action_v3.json
results/graph_action_v3_predictions.csv
results/graph_action_v3_baseline_predictions.csv
results/graph_action_v3_future_blind_registry.csv
```

Полный запуск:

```powershell
cd C:\Users\user\Desktop\info_graph_theory\complete_theory_kit
python run_complete_v2.py
```
---

## Spectral Graph Automata Field Theory v4

Добавлен новый слой `graph_automata_field_theory_v4.py`: единая теория поля переписана как графовая нейросетевая динамика с графовыми автоматами в базисе.

Главный объект:

```text
U_GNN = (G, L, X_t, A_theta, Phi_theta, R, exp(-sigma n), S_penalty)
```

Динамика:

```text
X_{t+1} = A(G, L, X_t; automata_basis)
O_k = Phi_theta(pool(X_T, L, heat_kernel))
```

Базис автоматов:

```text
identity_memory
laplacian_diffusion
neighbor_message
phase_rotation
spin_gate
color_gate
heat_kernel_gate
spectral_pool
```

Смысл redesign:

- поле заменено состоянием `X_t` на узлах графа;
- локальная динамика задается графовыми автоматами;
- `L` входит не декоративно, а через диффузию, message passing и pooling;
- физические наблюдаемые выводятся декодером `Phi_theta`;
- обучается только малый ridge-readout;
- `S_penalty` штрафует effective DOF, норму декодера, неиспользование автоматного базиса и утечку в blind-набор.

Машинный результат текущей версии:

```text
FAIL_BLIND_SCORE: fewer than 6 locked known-blind targets pass
effective_dof = 3.76296770442
automata_feature_count = 29
locked_known_blind = 0/10
```

Вывод: графово-нейросетевая форма построена и работает как проверяемое ядро, но текущий базис автоматов не является подтвержденной физической теорией.

Файлы результата:

```text
results/graph_automata_field_v4_report.md
results/graph_automata_field_v4.json
results/graph_automata_field_v4_predictions.csv
results/graph_automata_field_v4_baseline_predictions.csv
results/graph_automata_field_v4_future_blind_registry.csv
```
---

## BIP39 Unification Search v5

Добавлен экспериментальный слой `bip39_unification_search_v5.py`: он проверяет, можно ли собрать формулы и константы README через BIP39-инварианты.

Используются BIP39-числа:

```text
bits_per_word = 11
dictionary_size = 2048
words_per_phrase = 24
sha256_entropy_bits = 256
checksum_bits = 8
phrase_bits_total = 264
table_rows = 4
table_columns = 6
K = (11 + 1)/2 = 6
```

Проверены варианты:

```text
BIP39_EXACT_SECTOR
BIP39_K_ONLY_ORIGINAL_GRAPH
BIP39_SPARSE_MONOMIAL_NO_COEFFICIENT
BIP39_TARGET_CALIBRATED
```

Главный численный результат:

```text
BIP39_EXACT_SECTOR: 8/8
BIP39_K_ONLY_ORIGINAL_GRAPH: 9/11
BIP39_SPARSE_MONOMIAL_NO_COEFFICIENT: 11/11
BIP39_TARGET_CALIBRATED: 11/11
```

Самая интересная найденная ветка - `BIP39_SPARSE_MONOMIAL_NO_COEFFICIENT`: она попадает в 11/11 физических целей без target-specific численных коэффициентов. Примеры:

```text
alpha              = K^-1 * lnDict^-1 * U^-1
alpha_s            = K^-1 * bits^-1 * bip_density^-1
g_I^2              = K / lnDict
M_p                = m_e * pi * words^2
M_W                = m_e[GeV] * K * entropy * f1
M_Z                = m_e[GeV] * dict * total_bits / U
M_H                = m_e[GeV] * bits^2 * dict
sin2_thetaW        = lnK / checksum
G_F                = 1 / (pi * total_bits * f1)
Lambda_QCD         = U * bip_density / lnK
```

Честный статус:

```text
NUMERIC_HIT_WITH_LOOK_ELSEWHERE_RISK
```

Почему не финальное доказательство: формулы без коэффициентов, но каждая цель выбирала свой sparse-моном из пространства кандидатов. Следующий строгий шаг - заморозить правило выбора формулы заранее и проверить на новых blind targets.

Файлы результата:

```text
results/bip39_unification_search_v5_report.md
results/bip39_unification_search_v5.json
results/bip39_unification_search_v5_predictions.csv
```
---

## BIP39 No-Fit Verification v6

Добавлен строгий слой `bip39_no_fit_verification_v6.py`.

Отличие от v5:

```text
v5 = поиск формул
v6 = проверка замороженного реестра формул
```

В v6:

- поиск sparse-мономов выключен;
- target-specific коэффициенты запрещены;
- формулы заранее зашиты в `FROZEN_FORMULAS`;
- реестр формул имеет SHA256-хэш;
- наблюдаемые значения используются только на финальном этапе сравнения.

Текущий хэш реестра:

```text
d388fa65f2b74ffde9e313ee8334b11028eca6c02255da5a5b831fd9f8a0cbdb
```

Итог:

```text
PASS_README_TOLERANCE_ONLY: no fitting, but not all constants are within 1%
README log tolerance: 11/11
relative <= 1%: 7/11
relative <= 0.5%: 4/11
relative <= 0.1%: 0/11
```

Средняя относительная ошибка:

```text
0.899025251536 %
```

Максимальная относительная ошибка:

```text
1.75723248969 %
```

Самый честный вывод:

```text
BIP39 дает сильное no-fit численное попадание 11/11 по README-допускам,
но это не "абсолютная точность":
строгий порог 1% проходят 7/11,
0.5% проходят 4/11,
0.1% не проходит ни одна формула.
```

Файлы результата:

```text
results/bip39_no_fit_verification_v6_report.md
results/bip39_no_fit_verification_v6.json
results/bip39_no_fit_verification_v6.csv
```
---

## BIP39 All-Constants Benchmark v7

Добавлен большой стресс-тест `bip39_all_constants_benchmark_v7.py`.

Источник каталога:

```text
scipy.constants.physical_constants
```

Машинный объем проверки:

```text
positive constants tested: 387
dimensionless constants: 80
dimensional constants: 307
```

Строгая frozen no-fit модель BIP39 v6 покрывает только те величины, для которых заранее существует формула в замороженном реестре.

Итог frozen-покрытия:

```text
frozen_no_fit_predictions_available: 4/387
frozen_no_fit_predictions_pass_1_percent: 3/4
missing_frozen_formulas: 383
```

Это означает:

```text
FROZEN_BIP39_MODEL_DOES_NOT_COVER_300_PLUS_CONSTANTS
```

Также запущен диагностический sparse-поиск:

```text
sparse_search_candidate_count_per_constant: 101635
sparse_diagnostic_pass_1_percent_all_constants: 200/387
sparse_diagnostic_pass_1_percent_dimensionless: 58/80
```

Но этот sparse-поиск не считается доказательством, потому что формула выбирается после просмотра каждой цели. Это именно look-elsewhere diagnostic.

Особенно важно для размерных констант:

```text
dimensionless BIP39 monomial cannot predict SI dimensional numbers
without a declared physical unit basis.
```

Файлы результата:

```text
results/bip39_all_constants_benchmark_v7_report.md
results/bip39_all_constants_benchmark_v7.json
results/bip39_all_constants_benchmark_v7.csv
```
---

## BIP39 Fit All 445 Constants v8

Добавлен слой `bip39_fit_all_445_v8.py`.

Он делает именно подбор всех записей SciPy/CODATA:

```text
catalog_total_constants: 445
negative_constants_included: 58
dimensionless_constants: 128
dimensional_constants: 317
candidate_monomials_per_constant: 101635
```

Для каждой константы строится:

```text
signed BIP39 sparse monomial approximation
exact target-specific calibration coefficient
exact calibrated prediction
```

Результат:

```text
sparse_fit_pass_1_percent: 230/445
sparse_fit_pass_0_1_percent: 43/445
sparse_fit_pass_1_percent_dimensionless: 80/128
target_calibrated_exact_pass: 445/445
```

Вердикт:

```text
ALL_445_FITTED_DIAGNOSTICALLY
EXACT_445_REQUIRES_TARGET_SPECIFIC_COEFFICIENTS
```

То есть все 445 констант действительно подобраны в таблице v8, но точное 445/445 получается через индивидуальный коэффициент для каждой константы. Это полезная диагностическая карта, но не no-fit доказательство.

Файлы результата:

```text
results/bip39_fit_all_445_v8_report.md
results/bip39_fit_all_445_v8.json
results/bip39_fit_all_445_v8.csv
```
