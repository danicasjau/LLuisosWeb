/**
 * AE LLUÏSOS DE GRÀCIA - RETRO POSTER INTERACTIVITY & ENGINE
 */

document.addEventListener('DOMContentLoaded', () => {
  console.log("AE Lluïsos de Gràcia Web Engine Initialized");

  initNavHideToggle();
  //initNavAutoHide();
  initBarcode();
  initModalSystem();
  initCalendarViewer();
  initShopCart();

  setTimeout(handleHashExpansion, 300);
});

window.addEventListener('hashchange', handleHashExpansion);

/* ==========================================================================
   STATIC NAVIGATION MENU HIDE / SHOW TOGGLE
   ========================================================================== */
function initNavHideToggle() {
  const toggleBtn = document.getElementById('nav-hide-toggle');
  const navMenu = document.getElementById('main-nav');

  if (!toggleBtn || !navMenu) return;

  toggleBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    navMenu.classList.toggle('is-hidden');
    toggleBtn.classList.toggle('is-hidden-active');
  });
}

/* ==========================================================================
   AUTO-HIDE MENU ON INACTIVITY (5 SECONDS NO SCROLL)
   ========================================================================== */
function initNavAutoHide() {
  const navMenu = document.getElementById('main-nav');
  if (!navMenu) return;

  let scrollTimer = null;
  const HIDE_DELAY = 2000; // 5 seconds of inactivity

  function hideNav() {
    navMenu.classList.add('is-autohidden');
  }

  function showNav() {
    navMenu.classList.remove('is-autohidden');
  }

  function resetTimer() {
    showNav();
    if (scrollTimer) {
      clearTimeout(scrollTimer);
    }
    scrollTimer = setTimeout(hideNav, HIDE_DELAY);
  }

  // Listen to window scroll events to reveal menu and reset the 5-second timer
  window.addEventListener('scroll', resetTimer, { passive: true });

  // Pause auto-hide timer when user hovers over the navigation menu
  navMenu.addEventListener('mouseenter', () => {
    if (scrollTimer) clearTimeout(scrollTimer);
    showNav();
  });

  // Resume auto-hide timer when mouse leaves navigation menu
  navMenu.addEventListener('mouseleave', () => {
    resetTimer();
  });

  // Start initial 5-second timer on page load
  resetTimer();
}

/* ==========================================================================
   RETRO BARCODE GENERATOR
   ========================================================================== */
function initBarcode() {
  const barcodeContainer = document.getElementById('barcode-lines-container');
  if (!barcodeContainer) return;

  const pattern = [2, 1, 3, 1, 4, 1, 2, 2, 1, 3, 1, 1, 4, 2, 1, 3, 2, 1, 4, 1, 2, 1, 3, 1, 2, 4, 1, 2];
  barcodeContainer.innerHTML = '';

  pattern.forEach(width => {
    const bar = document.createElement('div');
    bar.className = 'barcode-bar';
    bar.style.width = `${width}px`;
    barcodeContainer.appendChild(bar);
  });
}

/* ==========================================================================
   MODAL POPUP SYSTEM
   ========================================================================== */
function initModalSystem() {
  const modalBackdrop = document.getElementById('retro-modal');
  const closeBtn = document.getElementById('modal-close-btn');

  if (!modalBackdrop) return;

  const closeModal = () => {
    modalBackdrop.classList.remove('active');
  };

  if (closeBtn) closeBtn.addEventListener('click', closeModal);

  modalBackdrop.addEventListener('click', (e) => {
    if (e.target === modalBackdrop) closeModal();
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeModal();
  });
}

function openModal(title, badge, dateLoc, content, imageSrc = null) {
  const modalBackdrop = document.getElementById('retro-modal');
  const titleEl = document.getElementById('modal-title');
  const badgeEl = document.getElementById('modal-badge');
  const metaEl = document.getElementById('modal-meta');
  const bodyEl = document.getElementById('modal-body');
  const imgEl = document.getElementById('modal-img');

  if (!modalBackdrop) return;

  titleEl.textContent = title;
  badgeEl.textContent = badge;
  metaEl.textContent = dateLoc;
  bodyEl.innerHTML = content;

  if (imageSrc && imgEl) {
    imgEl.src = imageSrc;
    imgEl.style.display = 'block';
  } else if (imgEl) {
    imgEl.style.display = 'none';
  }

  modalBackdrop.classList.add('active');
}

/* ==========================================================================
   CALENDAR & EVENT SYSTEM ENGINE (FULL 2026-2027 YEAR)
   ========================================================================== */
let calendarState = {
  currentYear: 2026,
  currentMonth: 9, // September
  filterUnit: 'all',
  activeView: 'month',
  selectedEventId: null
};

const MONTH_NAMES_CA = [
  "Gener", "Febrer", "Març", "Abril", "Maig", "Juny",
  "Juliol", "Agost", "Setembre", "Octubre", "Novembre", "Desembre"
];

const WEEKDAYS_CA = [
  "Diumenge", "Dilluns", "Dimarts", "Dimecres", "Dijous", "Divendres", "Dissabte"
];

function initCalendarViewer() {
  const monthGrid = document.getElementById('calendar-cells-grid');
  if (!monthGrid && !window.RAW_CALENDAR_EVENTS) return;

  // Initialize today's date context
  const now = new Date();
  // Default to September 2026 if before 2026-09 or after 2027-09
  if (now.getFullYear() === 2026 || now.getFullYear() === 2027) {
    calendarState.currentYear = now.getFullYear();
    calendarState.currentMonth = now.getMonth() + 1;
  } else {
    calendarState.currentYear = 2026;
    calendarState.currentMonth = 9;
  }

  // Ensure current month is within 2026-09 to 2027-09
  clampCalendarDate();

  // Close button for 2-div Day Modal
  const dayModalCloseBtn = document.getElementById('day-modal-close-btn');
  const dayModalBackdrop = document.getElementById('day-detail-modal');
  if (dayModalCloseBtn && dayModalBackdrop) {
    dayModalCloseBtn.addEventListener('click', () => {
      dayModalBackdrop.classList.remove('active');
    });
    dayModalBackdrop.addEventListener('click', (e) => {
      if (e.target === dayModalBackdrop) {
        dayModalBackdrop.classList.remove('active');
      }
    });
  }

  // Initial Renders
  updateSidebarUnitCounts();
  renderCalendarMonth();
  renderCalendarYear();
  renderUpcomingEvents();
}

function clampCalendarDate() {
  if (calendarState.currentYear < 2026) {
    calendarState.currentYear = 2026;
    calendarState.currentMonth = 9;
  } else if (calendarState.currentYear === 2026 && calendarState.currentMonth < 9) {
    calendarState.currentMonth = 9;
  } else if (calendarState.currentYear > 2027) {
    calendarState.currentYear = 2027;
    calendarState.currentMonth = 9;
  } else if (calendarState.currentYear === 2027 && calendarState.currentMonth > 9) {
    calendarState.currentMonth = 9;
  }
}

function getAllEvents() {
  return window.RAW_CALENDAR_EVENTS || [];
}

function getFilteredEvents() {
  const events = getAllEvents();
  if (calendarState.filterUnit === 'all') return events;

  return events.filter(ev => {
    const unitName = (ev.unit || '').toLowerCase();
    const filter = calendarState.filterUnit.toLowerCase();
    return unitName.includes(filter) || filter.includes(unitName);
  });
}

function updateSidebarUnitCounts() {
  const events = getAllEvents();
  const countAll = document.getElementById('count-all');
  const countCastors = document.getElementById('count-castors');
  const countLlops = document.getElementById('count-llops');
  const countRanguis = document.getElementById('count-ranguis');
  const countPios = document.getElementById('count-pios');
  const countTruk = document.getElementById('count-truk');
  const countGeneral = document.getElementById('count-general');
  const countMeg = document.getElementById('count-meg');

  if (!countAll) return;

  countAll.textContent = events.length;

  const countFor = (keyword) => events.filter(e => (e.unit || '').toLowerCase().includes(keyword.toLowerCase())).length;

  if (countCastors) countCastors.textContent = countFor('Castúdrigues');
  if (countLlops) countLlops.textContent = countFor('Dainops');
  if (countRanguis) countRanguis.textContent = countFor('Ranguis');
  if (countPios) countPios.textContent = countFor('Pionel·les');
  if (countTruk) countTruk.textContent = countFor('Truk');
  if (countGeneral) countGeneral.textContent = countFor('Assemblea');
  if (countMeg) countMeg.textContent = countFor('MEG');
}

function setCalendarUnitFilter(unitKeyword, btn) {
  calendarState.filterUnit = unitKeyword;
  document.querySelectorAll('.lateral-unit-btn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');

  renderCalendarMonth();
  renderCalendarYear();
  renderUpcomingEvents();
}

function prevMonth() {
  calendarState.currentMonth--;
  if (calendarState.currentMonth < 1) {
    calendarState.currentMonth = 12;
    calendarState.currentYear--;
  }
  clampCalendarDate();
  renderCalendarMonth();
}

function nextMonth() {
  calendarState.currentMonth++;
  if (calendarState.currentMonth > 12) {
    calendarState.currentMonth = 1;
    calendarState.currentYear++;
  }
  clampCalendarDate();
  renderCalendarMonth();
}

function onMonthDropdownChange(val) {
  if (!val) return;
  const [yearStr, monthStr] = val.split('-');
  calendarState.currentYear = parseInt(yearStr, 10);
  calendarState.currentMonth = parseInt(monthStr, 10);
  clampCalendarDate();
  renderCalendarMonth();
}

function setCalendarView(viewMode) {
  calendarState.activeView = viewMode;
  const monthContainer = document.getElementById('calendar-month-container');
  const yearContainer = document.getElementById('calendar-year-container');
  const btnMonth = document.getElementById('btn-view-month');
  const btnYear = document.getElementById('btn-view-year');

  if (viewMode === 'year') {
    if (monthContainer) monthContainer.style.display = 'none';
    if (yearContainer) yearContainer.style.display = 'block';
    if (btnMonth) btnMonth.classList.remove('active');
    if (btnYear) btnYear.classList.add('active');
    renderCalendarYear();
  } else {
    if (monthContainer) monthContainer.style.display = 'block';
    if (yearContainer) yearContainer.style.display = 'none';
    if (btnMonth) btnMonth.classList.add('active');
    if (btnYear) btnYear.classList.remove('active');
    renderCalendarMonth();
  }
}

function renderCalendarMonth() {
  const gridEl = document.getElementById('calendar-cells-grid');
  const headingEl = document.getElementById('current-month-heading');
  const selectEl = document.getElementById('month-dropdown-select');

  if (!gridEl) return;

  const y = calendarState.currentYear;
  const m = calendarState.currentMonth; // 1-12
  const monthFormatted = `${y}-${String(m).padStart(2, '0')}`;

  // Update Header & Dropdown
  const monthName = MONTH_NAMES_CA[m - 1];
  if (headingEl) {
    headingEl.textContent = `${monthName.toUpperCase()} ${y}`;
  }
  if (selectEl) {
    selectEl.value = monthFormatted;
  }

  // Determine first day of month (Monday = 0 ... Sunday = 6)
  const firstDayObj = new Date(y, m - 1, 1);
  let startDay = firstDayObj.getDay(); // Sunday=0, Monday=1, ...
  startDay = (startDay === 0) ? 6 : startDay - 1; // Convert to Monday=0

  const daysInMonth = new Date(y, m, 0).getDate();

  // Today string for comparison
  const now = new Date();
  const todayStr = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;

  const events = getFilteredEvents();

  gridEl.innerHTML = '';

  // Empty leading cells
  for (let i = 0; i < startDay; i++) {
    const emptyCell = document.createElement('div');
    emptyCell.className = 'calendar-cell empty';
    gridEl.appendChild(emptyCell);
  }

  // Days of current month
  for (let d = 1; d <= daysInMonth; d++) {
    const dayStr = `${y}-${String(m).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
    const isToday = (dayStr === todayStr);

    const cell = document.createElement('div');
    cell.className = `calendar-cell ${isToday ? 'is-today' : ''}`;
    cell.setAttribute('data-date', dayStr);

    // Find events on this day
    const dayEvents = events.filter(e => e.date === dayStr);
    if (dayEvents.length > 0) {
      cell.classList.add('has-events');
    }

    let topRowHtml = `
      <div class="cell-top-row">
        <span class="cell-number">${d}</span>
        ${isToday ? '<span class="today-pill-tag">AVUI</span>' : ''}
      </div>
    `;

    let eventsHtml = '<div class="cell-events-container">';
    dayEvents.slice(0, 3).forEach(ev => {
      const color = ev.badge_color || '#FF5722';
      eventsHtml += `
        <div class="cell-event-pill" style="background-color: ${color};" title="${escapeHtml(ev.title)}">
          ${escapeHtml(ev.title)}
        </div>
      `;
    });
    if (dayEvents.length > 3) {
      eventsHtml += `<div style="font-size:0.65rem; font-weight:800; color:var(--ink-muted); margin-top:2px;">+${dayEvents.length - 3} més</div>`;
    }
    eventsHtml += '</div>';

    cell.innerHTML = topRowHtml + eventsHtml;

    // Click to open 2-div Day Detail Modal
    cell.addEventListener('click', () => {
      openDayDetailModal(dayStr);
    });

    gridEl.appendChild(cell);
  }

  // Trailing empty cells to fill grid to multiple of 7
  const totalCells = startDay + daysInMonth;
  const remainder = totalCells % 7;
  if (remainder !== 0) {
    const needed = 7 - remainder;
    for (let i = 0; i < needed; i++) {
      const emptyCell = document.createElement('div');
      emptyCell.className = 'calendar-cell empty';
      gridEl.appendChild(emptyCell);
    }
  }
}

function renderCalendarYear() {
  const yearGrid = document.getElementById('year-months-grid');
  if (!yearGrid) return;

  const monthsList = [
    { y: 2026, m: 9 },
    { y: 2026, m: 10 },
    { y: 2026, m: 11 },
    { y: 2026, m: 12 },
    { y: 2027, m: 1 },
    { y: 2027, m: 2 },
    { y: 2027, m: 3 },
    { y: 2027, m: 4 },
    { y: 2027, m: 5 },
    { y: 2027, m: 6 },
    { y: 2027, m: 7 },
    { y: 2027, m: 8 },
    { y: 2027, m: 9 }
  ];

  const now = new Date();
  const todayStr = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;
  const events = getFilteredEvents();

  yearGrid.innerHTML = '';

  monthsList.forEach(({ y, m }) => {
    const card = document.createElement('div');
    card.className = 'mini-month-card';

    const monthName = MONTH_NAMES_CA[m - 1];
    const daysInMonth = new Date(y, m, 0).getDate();
    let startDay = new Date(y, m - 1, 1).getDay();
    startDay = (startDay === 0) ? 6 : startDay - 1;

    let cardHtml = `
      <div class="mini-month-title">
        <span>${monthName} ${y}</span>
        <button class="btn-retro" style="font-size:0.65rem; padding:2px 8px; border-radius:var(--small-br);" onclick="jumpToMonth(${y}, ${m})">VEURE MES →</button>
      </div>
      <div class="mini-month-grid">
        <div class="mini-day-header">DL</div>
        <div class="mini-day-header">DT</div>
        <div class="mini-day-header">DC</div>
        <div class="mini-day-header">DJ</div>
        <div class="mini-day-header">DV</div>
        <div class="mini-day-header">DS</div>
        <div class="mini-day-header">DM</div>
    `;

    for (let i = 0; i < startDay; i++) {
      cardHtml += `<div></div>`;
    }

    for (let d = 1; d <= daysInMonth; d++) {
      const dayStr = `${y}-${String(m).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
      const isToday = (dayStr === todayStr);
      const dayEvents = events.filter(e => e.date === dayStr);
      const hasEvent = dayEvents.length > 0;
      const dotColor = hasEvent ? (dayEvents[0].badge_color || '#FF5722') : 'transparent';

      cardHtml += `
        <div class="mini-day-cell ${isToday ? 'is-today' : ''} ${hasEvent ? 'has-event' : ''}" 
             onclick="openDayDetailModal('${dayStr}')" 
             title="${dayStr}${hasEvent ? ': ' + dayEvents.map(e => e.title).join(', ') : ''}">
          <span>${d}</span>
          ${hasEvent ? `<span class="mini-event-dot" style="background-color: ${dotColor};"></span>` : ''}
        </div>
      `;
    }

    cardHtml += `</div>`;
    card.innerHTML = cardHtml;
    yearGrid.appendChild(card);
  });
}

function jumpToMonth(y, m) {
  calendarState.currentYear = y;
  calendarState.currentMonth = m;
  setCalendarView('month');
}

/* ==========================================================================
   2-DIV CENTERED DAY POPUP MODAL LOGIC
   ========================================================================== */
function openDayDetailModal(dateStr, preselectedEventId = null) {
  const modal = document.getElementById('day-detail-modal');
  const dayNumEl = document.getElementById('day-modal-day-num');
  const weekdayEl = document.getElementById('day-modal-weekday');
  const dateTextEl = document.getElementById('day-modal-date-text');
  const listEl = document.getElementById('day-modal-events-list');
  const detailEl = document.getElementById('day-modal-event-detail');

  if (!modal || !dateStr) return;

  const [yStr, mStr, dStr] = dateStr.split('-');
  const y = parseInt(yStr, 10);
  const m = parseInt(mStr, 10);
  const d = parseInt(dStr, 10);

  const dateObj = new Date(y, m - 1, d);
  const weekday = WEEKDAYS_CA[dateObj.getDay()].toUpperCase();
  const monthName = MONTH_NAMES_CA[m - 1];

  if (dayNumEl) dayNumEl.textContent = d;
  if (weekdayEl) weekdayEl.textContent = weekday;
  if (dateTextEl) dateTextEl.textContent = `${d} de ${monthName} de ${y}`;

  const allEvents = getAllEvents();
  const dayEvents = allEvents.filter(e => e.date === dateStr);

  // Populate Left Div List
  listEl.innerHTML = '';
  if (dayEvents.length === 0) {
    listEl.innerHTML = `
      <div style="padding: 25px 15px; text-align: center; color: var(--ink-muted); background: #FFF; border-radius: var(--nor-br); border: 1px dashed var(--border-dark);">
        <strong style="display:block; font-size: 0.95rem; color: var(--ink-black); margin-bottom: 4px;">Sense sortides programades</strong>
        <p style="font-size: 0.82rem; margin: 0;">No hi ha cap esdeveniment per a aquesta data al calendari oficial.</p>
      </div>
    `;
    detailEl.innerHTML = `
      <div style="padding: 30px 20px; text-align: center; color: var(--ink-muted); display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%;">
        <h4 style="font-family: var(--font-title); font-size: 1.2rem; color: var(--ink-black); margin-bottom: 6px;">AE Lluïsos de Gràcia</h4>
        <p style="font-size: 0.85rem; line-height: 1.5;">Selecciona un altre dia amb activitat al calendari per consultar els horaris, lloc i fitxa educativa de l'esdeveniment.</p>
      </div>
    `;
  } else {
    // Determine active event
    let activeEvent = dayEvents[0];
    if (preselectedEventId) {
      const found = dayEvents.find(e => e.id === preselectedEventId || String(e.id) === String(preselectedEventId));
      if (found) activeEvent = found;
    }

    dayEvents.forEach(ev => {
      const isActive = (ev.id === activeEvent.id);
      const row = document.createElement('div');
      row.className = `day-event-row ${isActive ? 'active' : ''}`;
      row.innerHTML = `
        <div class="day-event-row-top">
          <span class="day-event-row-title">${escapeHtml(ev.title)}</span>
          <span class="event-hours-badge">${escapeHtml(ev.time || 'Horari a confirmar')}</span>
        </div>
        <div>
          <span class="day-event-row-unit" style="background-color: ${ev.badge_color || '#FF5722'};">${escapeHtml(ev.unit || 'General')}</span>
        </div>
      `;

      row.addEventListener('click', () => {
        document.querySelectorAll('.day-event-row').forEach(r => r.classList.remove('active'));
        row.classList.add('active');
        renderDayModalDetail(ev);
      });

      listEl.appendChild(row);
    });

    renderDayModalDetail(activeEvent);
  }

  modal.classList.add('active');
}

function renderDayModalDetail(ev) {
  const detailEl = document.getElementById('day-modal-event-detail');
  if (!detailEl || !ev) return;

  const imgSrc = ev.image || '/static/images/backgroundmountains.png';
  const color = ev.badge_color || '#FF5722';

  detailEl.innerHTML = `
    <div class="day-detail-card">
      <img src="${imgSrc}" alt="${escapeHtml(ev.title)}" class="day-detail-img" onerror="this.src='/static/images/backgroundmountains.png';">
      <div class="day-detail-header-badges">
        <span class="day-detail-unit-tag" style="background-color: ${color};">${escapeHtml(ev.unit || 'General')}</span>
        <span class="day-detail-time-tag">${escapeHtml(ev.time || 'Horari per concretar')}</span>
      </div>
      <h3 class="day-detail-title">${escapeHtml(ev.title)}</h3>
      <div class="day-detail-loc">${escapeHtml(ev.location || 'Local Lluïsos de Gràcia')}</div>
      <div class="day-detail-desc">${escapeHtml(ev.description || 'Sense descripció addicional.')}</div>
    </div>
  `;
}

/* ==========================================================================
   UPCOMING EVENTS (NEXT 6 EVENTS) WITH DAYS LEFT & IMAGES
   ========================================================================== */
function calculateDaysLeft(dateStr) {
  if (!dateStr) return { text: "PROGRAMAT", days: 999 };
  const target = new Date(dateStr + "T00:00:00");
  const now = new Date();
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());

  const diffTime = target.getTime() - today.getTime();
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

  if (diffDays === 0) return { text: "AVUI", days: 0 };
  if (diffDays === 1) return { text: "DEMÀ", days: 1 };
  if (diffDays > 1) return { text: `FALTEN ${diffDays} DIES`, days: diffDays };
  return { text: "PASSAT", days: diffDays };
}

function renderUpcomingEvents() {
  const container = document.getElementById('next-6-events-container');
  if (!container) return;

  const events = getFilteredEvents();
  const now = new Date();
  const todayStr = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;

  // Sort upcoming events chronologically
  const sorted = [...events].sort((a, b) => a.date.localeCompare(b.date));

  // Find events from today onwards, or take next available
  let upcoming = sorted.filter(e => e.date >= todayStr);
  if (upcoming.length < 6) {
    upcoming = sorted; // Fallback to entire list if in past
  }
  const next6 = upcoming.slice(0, 6);

  container.innerHTML = '';

  next6.forEach(ev => {
    const daysInfo = calculateDaysLeft(ev.date);
    const card = document.createElement('div');
    card.className = 'upcoming-event-card';

    const imgSrc = ev.image || '/static/images/backgroundmountains.png';
    const color = ev.badge_color || '#FF5722';

    // Format human readable Catalan date: "12 Set 2026"
    const [y, m, d] = ev.date.split('-');
    const mName = MONTH_NAMES_CA[parseInt(m, 10) - 1].substring(0, 3);
    const formattedDate = `${parseInt(d, 10)} ${mName} ${y}`;

    card.innerHTML = `
      <div class="event-card-banner-wrap">
        <img src="${imgSrc}" alt="${escapeHtml(ev.title)}" class="event-card-img" onerror="this.src='/static/images/backgroundmountains.png';">
        <span class="event-card-days-left-badge">${daysInfo.text}</span>
        <span class="event-card-unit-badge" style="background-color: ${color};">${escapeHtml(ev.unit || 'General')}</span>
      </div>
      <div class="event-card-body">
        <div>
          <h4 class="event-card-title">${escapeHtml(ev.title)}</h4>
          <div class="event-card-timeloc">${formattedDate} &nbsp;•&nbsp; ${escapeHtml(ev.time || '')}</div>
          <div class="event-card-timeloc" style="margin-top:2px;">${escapeHtml(ev.location || 'Local del Cau')}</div>
          <p class="event-card-desc" style="margin-top:8px;">${escapeHtml(ev.description || '')}</p>
        </div>
        <div class="event-card-action">
          <span>VEURE FITXA I HORARIS</span>
          <span>→</span>
        </div>
      </div>
    `;

    card.addEventListener('click', () => {
      openDayDetailModal(ev.date, ev.id);
    });

    container.appendChild(card);
  });
}

function downloadCalendarPDF() {
  showCartToast("Preparant el document PDF del calendari...");
  setTimeout(() => {
    window.print();
  }, 400);
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}


/* ==========================================================================
   SHOPPING CART SYSTEM FOR BOTIGA
   ========================================================================== */
let cart = [];

function initShopCart() {
  const cartButtons = document.querySelectorAll('.btn-add-cart');
  const cartCounter = document.getElementById('cart-counter');

  cartButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      const id = btn.getAttribute('data-id');
      const name = btn.getAttribute('data-name');
      const price = parseFloat(btn.getAttribute('data-price'));

      cart.push({ id, name, price });
      if (cartCounter) cartCounter.textContent = cart.length;

      showCartToast(`Afegit a la cesta: ${name}`);
    });
  });
}

function showCartToast(msg) {
  let toast = document.getElementById('cart-toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'cart-toast';
    toast.style.cssText = `
      position: fixed;
      bottom: 25px;
      right: 25px;
      background: #FF5722;
      color: white;
      padding: 12px 20px;
      border: 1px solid rgba(18, 18, 18, 0.2);
      border-radius: 12px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.15);
      font-family: 'Space Grotesk', sans-serif;
      font-weight: 700;
      z-index: 2000;
      transition: all 0.3s ease;
    `;
    document.body.appendChild(toast);
  }
  toast.textContent = msg;
  toast.style.opacity = '1';

  setTimeout(() => {
    toast.style.opacity = '0';
  }, 2500);
}

/* ==========================================================================
   HASH SHORTCUT AUTO-SCROLL (e.g. /#distinction-qui-som, /#qui-som)
   ========================================================================== */
function handleHashExpansion() {
  const hash = window.location.hash;
  if (!hash) return;

  const targetEl = document.querySelector(hash);
  if (targetEl) {
    targetEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
}

