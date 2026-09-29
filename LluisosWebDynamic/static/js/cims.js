/**
 * cims.js - Dynamic Peak Catalog and Unit Filtering
 * AE Lluïsos de Gràcia
 *
 * Reads cims from /static/data/cims.json (or /api/cims),
 * dynamically generates the peak list HTML inside .peaks-grid,
 * and handles unit filtering with authentic branca color states.
 */

(function () {
  'use strict';

  // Unit / Branca Color Tokens
  const PEAK_LEVEL_COLORS = {
    CiLL: '#F97316', // Castúdrigues - Orange
    LLiD: '#FACC15', // Dainops - Yellow
    RNG: '#2563EB',  // Ranguis - Blue
    PiC: '#DC2626',  // Pionel·les - Red
    Truk: '#16A34A'  // Truk - Green
  };

  // Unit Names
  const PEAK_LEVEL_NAMES = {
    CiLL: 'Castúdrigues',
    LLiD: 'Dainops',
    RNG: 'Ranguis',
    PiC: 'Pionel·les',
    Truk: 'Truk'
  };

  // Fallback seed of 60 peaks in case of network issues
  const FALLBACK_CIMS = [
    { "id": "01", "number": 1, "name": "Bastiments", "levels": ["RNG", "PiC"], "levels_label": "RNG / PiC" },
    { "id": "02", "number": 2, "name": "Besiberri Sud", "levels": ["PiC", "Truk"], "levels_label": "PiC / Truk" },
    { "id": "03", "number": 3, "name": "Canigó", "levels": ["LLiD", "Truk"], "levels_label": "LLiD / Truk" },
    { "id": "04", "number": 4, "name": "Cap de la Gallina Pelada", "levels": ["RNG"], "levels_label": "RNG" },
    { "id": "05", "number": 5, "name": "Carlit", "levels": ["PiC"], "levels_label": "PiC" },
    { "id": "06", "number": 6, "name": "Castell de Burriac", "levels": ["CiLL", "LLiD"], "levels_label": "CiLL / LLiD" },
    { "id": "07", "number": 7, "name": "Cogulló d'Estela", "levels": ["LLiD", "RNG"], "levels_label": "LLiD / RNG" },
    { "id": "08", "number": 8, "name": "Comabona", "levels": ["LLiD"], "levels_label": "LLiD" },
    { "id": "09", "number": 9, "name": "Comanegra", "levels": ["LLiD"], "levels_label": "LLiD" },
    { "id": "10", "number": 10, "name": "Comapedrosa", "levels": ["RNG"], "levels_label": "RNG" },
    { "id": "11", "number": 11, "name": "El Negrell", "levels": ["CiLL"], "levels_label": "CiLL" },
    { "id": "12", "number": 12, "name": "El Salabardar", "levels": ["LLiD"], "levels_label": "LLiD" },
    { "id": "13", "number": 13, "name": "L'Espina", "levels": ["RNG"], "levels_label": "RNG" },
    { "id": "14", "number": 14, "name": "La Mola de Sant Llorenç del Munt", "levels": ["LLiD"], "levels_label": "LLiD" },
    { "id": "15", "number": 15, "name": "La Talaia de Montmell", "levels": ["LLiD"], "levels_label": "LLiD" },
    { "id": "16", "number": 16, "name": "Matagalls", "levels": ["LLiD", "PiC"], "levels_label": "LLiD / PiC" },
    { "id": "17", "number": 17, "name": "Mont-Roig", "levels": ["RNG"], "levels_label": "RNG" },
    { "id": "18", "number": 18, "name": "Montardo", "levels": ["RNG"], "levels_label": "RNG" },
    { "id": "19", "number": 19, "name": "Montcau", "levels": ["CiLL"], "levels_label": "CiLL" },
    { "id": "20", "number": 20, "name": "Monteixo", "levels": ["LLiD", "RNG", "PiC"], "levels_label": "LLiD / RNG / PiC" },
    { "id": "21", "number": 21, "name": "Muntanya del Montgrí", "levels": ["CiLL", "LLiD"], "levels_label": "CiLL / LLiD" },
    { "id": "22", "number": 22, "name": "Noufonts", "levels": ["RNG"], "levels_label": "RNG" },
    { "id": "23", "number": 23, "name": "Pedraforca", "levels": ["RNG"], "levels_label": "RNG" },
    { "id": "24", "number": 24, "name": "Penya Sant Alís", "levels": ["CiLL", "LLiD"], "levels_label": "CiLL / LLiD" },
    { "id": "25", "number": 25, "name": "Penyagolosa", "levels": ["LLiD"], "levels_label": "LLiD" },
    { "id": "26", "number": 26, "name": "Penyes Altes de Moixeró", "levels": ["RNG", "PiC"], "levels_label": "RNG / PiC" },
    { "id": "27", "number": 27, "name": "Perdiguero", "levels": ["Truk"], "levels_label": "Truk" },
    { "id": "28", "number": 28, "name": "Pic d'Amitges", "levels": ["PiC"], "levels_label": "PiC" },
    { "id": "29", "number": 29, "name": "Pic d'Aneto", "levels": ["Truk"], "levels_label": "Truk" },
    { "id": "30", "number": 30, "name": "Pic d'Eina", "levels": ["RNG", "PiC"], "levels_label": "RNG / PiC" },
    { "id": "31", "number": 31, "name": "Pic de l'Infern", "levels": ["PiC", "Truk"], "levels_label": "PiC / Truk" },
    { "id": "32", "number": 32, "name": "Pic de Subenuix", "levels": ["PiC"], "levels_label": "PiC" },
    { "id": "33", "number": 33, "name": "Pica d'Estats", "levels": ["PiC", "Truk"], "levels_label": "PiC / Truk" },
    { "id": "34", "number": 34, "name": "Pica Roja", "levels": ["RNG"], "levels_label": "RNG" },
    { "id": "35", "number": 35, "name": "Posets", "levels": ["Truk"], "levels_label": "Truk" },
    { "id": "36", "number": 36, "name": "Puig de Bassegoda", "levels": ["LLiD", "RNG", "PiC"], "levels_label": "LLiD / RNG / PiC" },
    { "id": "37", "number": 37, "name": "Puig de Massanella", "levels": ["RNG"], "levels_label": "RNG" },
    { "id": "38", "number": 38, "name": "Puig dels Bufadors", "levels": ["LLiD"], "levels_label": "LLiD" },
    { "id": "39", "number": 39, "name": "Puig Pedrós", "levels": ["PiC"], "levels_label": "PiC" },
    { "id": "40", "number": 40, "name": "Puig Peric", "levels": ["PiC"], "levels_label": "PiC" },
    { "id": "41", "number": 41, "name": "Puigllançada", "levels": ["CiLL", "LLiD", "PiC"], "levels_label": "CiLL / LLiD / PiC" },
    { "id": "42", "number": 42, "name": "Puigmal", "levels": ["RNG", "PiC"], "levels_label": "RNG / PiC" },
    { "id": "43", "number": 43, "name": "Puigsacalm", "levels": ["LLiD", "RNG", "PiC"], "levels_label": "LLiD / RNG / PiC" },
    { "id": "44", "number": 44, "name": "Puigsagordi", "levels": ["PiC"], "levels_label": "PiC" },
    { "id": "45", "number": 45, "name": "Punta Alta", "levels": ["PiC"], "levels_label": "PiC" },
    { "id": "46", "number": 46, "name": "Roques de Sant Benet", "levels": ["CiLL"], "levels_label": "CiLL" },
    { "id": "47", "number": 47, "name": "Sant Jeroni", "levels": ["LLiD"], "levels_label": "LLiD" },
    { "id": "48", "number": 48, "name": "Sant Mamet", "levels": ["LLiD", "RNG"], "levels_label": "LLiD / RNG" },
    { "id": "49", "number": 49, "name": "Sant Salvador de les Espases", "levels": ["CiLL", "LLiD"], "levels_label": "CiLL / LLiD" },
    { "id": "50", "number": 50, "name": "Sant Salvador de Saverdera", "levels": ["CiLL", "LLiD"], "levels_label": "CiLL / LLiD" },
    { "id": "51", "number": 51, "name": "Taga", "levels": ["CiLL", "RNG", "PiC"], "levels_label": "CiLL / RNG / PiC" },
    { "id": "52", "number": 52, "name": "Tagamanent", "levels": ["LLiD"], "levels_label": "LLiD" },
    { "id": "53", "number": 53, "name": "Tibidabo", "levels": ["LLiD", "Truk"], "levels_label": "LLiD / Truk" },
    { "id": "54", "number": 54, "name": "Tossa d'Alp", "levels": ["LLiD", "RNG"], "levels_label": "LLiD / RNG" },
    { "id": "55", "number": 55, "name": "Tossa Plana de Lles", "levels": ["PiC"], "levels_label": "PiC" },
    { "id": "56", "number": 56, "name": "Tossal de la Baltasana", "levels": ["CiLL", "LLiD"], "levels_label": "CiLL / LLiD" },
    { "id": "57", "number": 57, "name": "Tossal dels Tres Reis", "levels": ["LLiD", "PiC"], "levels_label": "LLiD / PiC" },
    { "id": "58", "number": 58, "name": "Tuc de Ratera", "levels": ["PiC"], "levels_label": "PiC" },
    { "id": "59", "number": 59, "name": "Turó de l'Home", "levels": ["RNG"], "levels_label": "RNG" },
    { "id": "60", "number": 60, "name": "Volcà de Santa Margarida", "levels": ["CiLL"], "levels_label": "CiLL" }
  ];

  /**
   * Build a single peak <li> element matching style.css expectations
   */
  function createPeakItemElement(peak) {
    const li = document.createElement('li');
    li.className = 'peak-item';

    const levels = Array.isArray(peak.levels)
      ? peak.levels
      : (typeof peak.levels === 'string' ? peak.levels.trim().split(/\s+/) : []);

    li.dataset.levels = levels.join(' ');

    // Number circle: 01, 02, etc.
    const numSpan = document.createElement('span');
    numSpan.className = 'peak-number';
    const num = peak.id || (peak.number ? String(peak.number).padStart(2, '0') : '00');
    numSpan.textContent = String(num).padStart(2, '0');

    // Peak name
    const strong = document.createElement('strong');
    strong.textContent = peak.name;

    // Levels label / dots container
    const labelSpan = document.createElement('span');
    labelSpan.className = 'peak-levels-label';

    const dotsSpan = document.createElement('span');
    dotsSpan.className = 'peak-level-dots';
    const unitLabels = levels.map(l => PEAK_LEVEL_NAMES[l] || l).join(', ');
    dotsSpan.setAttribute('aria-label', `Unitats: ${unitLabels}`);

    levels.forEach(level => {
      const dot = document.createElement('span');
      dot.className = 'peak-level-dot';
      dot.title = PEAK_LEVEL_NAMES[level] || level;
      dot.style.backgroundColor = PEAK_LEVEL_COLORS[level] || '#94A3B8';
      dotsSpan.appendChild(dot);
    });

    labelSpan.appendChild(dotsSpan);

    li.appendChild(numSpan);
    li.appendChild(strong);
    li.appendChild(labelSpan);

    return li;
  }

  /**
   * Render list of peaks into the DOM container
   */
  function renderPeaks(peaks) {
    const container = document.getElementById('peaks-container') || document.querySelector('.peaks-grid');
    if (!container) return;

    container.innerHTML = '';
    const fragment = document.createDocumentFragment();

    peaks.forEach(peak => {
      fragment.appendChild(createPeakItemElement(peak));
    });

    container.appendChild(fragment);

    // Apply active filter if one was already clicked
    applyCurrentFilter();
  }

  /**
   * Apply currently selected filter to all peak items
   */
  function applyCurrentFilter() {
    const activeBtn = document.querySelector('.equips-filters-strip .btn-filter.active, .peaks-filters .btn-filter.active, .peak-filter.active');
    const selectedLevel = activeBtn ? (activeBtn.dataset.level || 'all') : 'all';

    const items = document.querySelectorAll('.peak-item');
    items.forEach(item => {
      const levels = (item.dataset.levels || '').split(' ').filter(Boolean);
      const isVisible = (selectedLevel === 'all') || levels.includes(selectedLevel);

      if (isVisible) {
        item.hidden = false;
        item.removeAttribute('hidden');
        item.style.display = '';
      } else {
        item.hidden = true;
        item.setAttribute('hidden', '');
        item.style.display = 'none';
      }
    });
  }

  /**
   * Initialize filter button click listeners
   */
  function setupFilters() {
    const filterButtons = document.querySelectorAll('.equips-filters-strip .btn-filter, .peak-filter');
    if (!filterButtons.length) return;

    filterButtons.forEach(btn => {
      btn.addEventListener('click', function () {
        // Toggle active class on buttons
        filterButtons.forEach(b => {
          b.classList.remove('active', 'is-active');
        });
        this.classList.add('active', 'is-active');

        // Apply filter immediately
        applyCurrentFilter();
      });
    });
  }

  /**
   * Fetch JSON from /static/data/cims.json (with /api/cims and FALLBACK_CIMS backups)
   */
  async function loadPeaksData() {
    // Check if we can fetch the JSON
    let data = null;

    try {
      const resp = await fetch('/static/data/cims.json');
      if (resp.ok) {
        data = await resp.json();
      } else {
        throw new Error(`HTTP ${resp.status}`);
      }
    } catch (err1) {
      console.warn('Direct static/data/cims.json fetch unsuccessful, trying /api/cims...', err1);
      try {
        const resp2 = await fetch('/api/cims');
        if (resp2.ok) {
          data = await resp2.json();
        }
      } catch (err2) {
        console.warn('API /api/cims fetch unsuccessful, using embedded dataset...', err2);
      }
    }

    if (Array.isArray(data) && data.length > 0) {
      renderPeaks(data);
    } else {
      renderPeaks(FALLBACK_CIMS);
    }
  }

  // Initialize on DOMContentLoaded or immediately if DOM is already parsed
  function init() {
    setupFilters();
    loadPeaksData();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
