# Panel Analityczny rNPS · mBank 2026

Interaktywny panel analityczny odpowiadający na wymagania Części A briefu NPS 2026 mBank.

## Zawartość panelu

| Zakładka | Opis |
|----------|------|
| 🗺️ Mapa wpływ × incydencja | Macierz 2×2 epizodów: siła wpływu na rNPS vs częstość kontaktu |
| 🔮 Symulator Co-jeśli | Waterfall chart: symulacja wzrostu rNPS przy poprawie wybranych epizodów |
| 📊 Ranking driverów | Wpływ bezpośredni i pośredni, luka jakościowa (ocena vs impact) |
| 📈 Ranking NPS & trendy | Trend miesięczny, benchmark konkurencyjny, segmentacja wg wieku/kanału/relacji |
| 📤 Dane & eksport | Surowe dane respondentów + CSV/XLSX gotowe do Power BI / SQL / Pandas |

## Uruchomienie

```bash
# 1. Instalacja zależności
pip install -r requirements.txt

# 2. Uruchomienie aplikacji
streamlit run app.py
```

Panel otworzy się automatycznie w przeglądarce pod adresem http://localhost:8501

## Struktura projektu

```
nps_panel/
├── app.py                    # Główna aplikacja Streamlit
├── requirements.txt          # Zależności Python
├── README.md
├── data/
│   ├── generate_data.py      # Generator danych demonstracyjnych
│   ├── respondents.csv       # Dane respondentów (8 000 rekordów)
│   ├── drivers.csv           # Tabela driverów NPS (16 epizodów)
│   └── monthly_ranking.csv   # Ranking miesięczny (12 miesięcy × 8 banków)
└── modules/
    ├── filters.py            # Sidebar z filtrami
    ├── impact_map.py         # Mapa wpływ × incydencja
    ├── whatif.py             # Symulator Co-jeśli
    ├── drivers.py            # Ranking driverów
    ├── ranking.py            # Ranking NPS & trendy
    └── export.py             # Eksport CSV/XLSX + Data Dictionary
```

## Filtry

- 🏦 Bank (mBank + 7 banków konkurencyjnych)
- 📅 Miesiąc (styczeń–grudzień 2025)
- 👤 Wiek (5 przedziałów: 15-18, 18-20, 21-27, 28-40, 40+)
- 📱 Kanał (mobile, web, CC, oddział)
- 🔗 Relacja (główna / dodatkowa)

## Dane

Dane demonstracyjne wygenerowane losowo (seed=42) dla celów przetargowych.
W produkcji zastąpić plikami CSV/XLSX dostarczanymi przez agencję badawczą.

Format pliku respondentów zgodny z wymogami briefu:
- dane niezagregowane (jeden wiersz = jeden respondent)
- gotowe do importu w Microsoft SQL Server, Power BI, Python Pandas
