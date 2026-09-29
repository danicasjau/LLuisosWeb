/**
 * AE LLUÏSOS DE GRÀCIA - KINIELA ESCOLTA ENGINE 2026-2027
 * Interactive Group Assignment Engine & Secure Backend Storage
 */

// 6 Scout units for the 2026-2027 scout year
const GROUPS = [
  { code: "castors", name: "Castúdrigues", color: "#F97316", badgeColor: "#EA580C" },
  { code: "llops", name: "Dainops", color: "#F59E0B", badgeColor: "#D97706" },
  { code: "ranguis", name: "Ranguis", color: "#0284C7", badgeColor: "#0369A1" },
  { code: "pios", name: "Pionel·les", color: "#E11D48", badgeColor: "#BE123C" },
  { code: "truk", name: "Truk", color: "#059669", badgeColor: "#047857" },
  { code: "marxen", name: "Marxen", color: "#7C3AED", badgeColor: "#6D28D9" }
];

// 7 New Caps (Truks)
const NEW_CAPS = [
  { id: 1001, name: "Pau Nuet", isNewCap: true },
  { id: 1002, name: "Joan Nuet", isNewCap: true },
  { id: 1003, name: "Jana Bosc", isNewCap: true },
  { id: 1004, name: "Iris de Cook", isNewCap: true },
  { id: 1005, name: "Aniol Rovira", isNewCap: true },
  { id: 1006, name: "Júlia Muntada", isNewCap: true },
  { id: 1007, name: "Aina Franquesa", isNewCap: true }
];

// Active pool of all 29 members
let MEMBERS_POOL = [];
// State: memberId -> groupCode (or 'pool')
let assignments = {};
document.addEventListener('DOMContentLoaded', () => {
  console.log("⚡ Kiniela Escolta Engine Initialized");
  initKiniela();
});

function initKiniela() {
  MEMBERS_POOL = [];

  // 1. Populate from backend team data if available
  if (Array.isArray(window.CAPS_POOL) && window.CAPS_POOL.length > 0) {
    window.CAPS_POOL.forEach(member => {
      MEMBERS_POOL.push({
        id: member.id,
        name: member.name,
        photo: member.image || '/static/images/scout_team.jpg',
        role: member.role || '',
        unit: member.unit || '',
        years: member.years || '',
        bio: member.bio || '',
        quote: member.quote || '',
        isNewCap: false
      });
    });
  } else {
    // Fallback seed
    const DEFAULT_EXISTING = [
      "Marc Vila", "Larraitz Echeverria", "Guillem Pujol", "Aina Fontcuberta",
      "Pol Serra", "Clara Rius", "Pau Soler", "Meritxell Balaguer", "Ignasi Mas",
      "Berta Canal", "Arnau Puig", "Laia Domènech", "Gerard Farré", "Mireia Rovira",
      "Oriol Noguera", "Judit Camps", "Xavi Vidal", "Núria Comas", "Ferran Dalmau",
      "Eulàlia Costa", "Bernat Badia", "Gemma Fortuny"
    ];
    DEFAULT_EXISTING.forEach((name, idx) => {
      MEMBERS_POOL.push({
        id: idx + 1,
        name: name,
        photo: '/static/images/scout_team.jpg',
        role: 'Cap',
        isNewCap: false
      });
    });
  }

  // 2. Add New Caps (Truks)
  NEW_CAPS.forEach(member => {
    MEMBERS_POOL.push({
      ...member,
      photo: '/static/images/backgroundmountains.png'
    });
  });

  resetAssignments();
  renderGroupsUI();
  renderPoolUI();
  setupActionButtons();
  setupSearchFilter();
}

function resetAssignments() {
  assignments = {};
  MEMBERS_POOL.forEach(m => {
    assignments[m.id] = 'pool';
  });
}

/* ==========================================================================
   UI RENDERING (GROUPS & POOL)
   ========================================================================== */

function renderPoolUI() {
  const poolContainer = document.getElementById('unassigned-pool');
  if (!poolContainer) return;

  // Setup lateral dropzone once
  if (!poolContainer.dataset.dropReady) {
    poolContainer.addEventListener('dragover', handleDragOver);
    poolContainer.addEventListener('dragleave', handleDragLeave);
    poolContainer.addEventListener('drop', (e) => handleDrop(e, 'pool'));
    poolContainer.dataset.dropReady = 'true';
  }

  poolContainer.innerHTML = '';

  const searchVal = (document.getElementById('pool-search-input')?.value || '').toLowerCase().trim();
  const unassigned = MEMBERS_POOL.filter(m => assignments[m.id] === 'pool');

  const counterBadge = document.getElementById('sidebar-pool-count');
  if (counterBadge) counterBadge.textContent = unassigned.length;

  if (unassigned.length === 0) {
    poolContainer.innerHTML = `
      <div style="background:#ECFDF5; border:1px solid #10B981; color:#065F46; padding:16px; border-radius:8px; text-align:center; font-weight:700; font-size:0.92rem;">
        ✓ Tots els caps han estat assignats!
      </div>
    `;
    return;
  }

  const existingCaps = unassigned.filter(m => !m.isNewCap);
  const newCaps = unassigned.filter(m => m.isNewCap);

  // Existing Caps List
  existingCaps
    .filter(m => !searchVal || m.name.toLowerCase().includes(searchVal))
    .forEach(member => {
      poolContainer.appendChild(createMemberCard(member));
    });

  // New Caps Section
  const filteredNewCaps = newCaps.filter(m => !searchVal || m.name.toLowerCase().includes(searchVal));
  if (filteredNewCaps.length > 0) {
    const divider = document.createElement('div');
    divider.className = 'kiniela-new-caps-title';
    divider.textContent = 'TRUKS';
    poolContainer.appendChild(divider);

    filteredNewCaps.forEach(member => {
      poolContainer.appendChild(createMemberCard(member));
    });
  }
}

function renderGroupsUI() {
  const groupsContainer = document.getElementById('groups-container');
  if (!groupsContainer) return;

  groupsContainer.innerHTML = '';

  GROUPS.forEach(group => {
    const groupCol = document.createElement('div');
    groupCol.className = 'group-column';
    groupCol.setAttribute('data-group', group.code);
    groupCol.style.setProperty('--group-color', group.color);

    const membersInGroup = MEMBERS_POOL.filter(m => assignments[m.id] === group.code);

    groupCol.innerHTML = `
      <div class="group-header" style="background-color: ${group.color}; display: flex; justify-content: space-between; align-items: center;">
        <div>
          <div class="group-title">${group.name}</div>
        </div>
        <span class="group-count-badge" style="background: rgba(0,0,0,0.25); color: #fff; padding: 2px 10px; border-radius: 999px; font-weight: 800; font-size: 0.85rem;">
          ${membersInGroup.length}
        </span>
      </div>
      <div class="group-dropzone" data-group="${group.code}" id="dropzone-${group.code}">
      </div>
    `;

    const dropzone = groupCol.querySelector('.group-dropzone');
    dropzone.addEventListener('dragover', handleDragOver);
    dropzone.addEventListener('dragleave', handleDragLeave);
    dropzone.addEventListener('drop', (e) => handleDrop(e, group.code));

    if (membersInGroup.length === 0) {
      dropzone.innerHTML = `
        <div style="color: #94A3B8; font-size: 0.85rem; text-align: center; margin: auto; padding: 20px 10px; border: 2px dashed #E2E8F0; border-radius: 8px;">
          Arrossega un cap aquí
        </div>
      `;
    } else {
      membersInGroup.forEach(member => {
        dropzone.appendChild(createMemberCard(member, true));
      });
    }

    groupsContainer.appendChild(groupCol);
  });
}

function createMemberCard(member, isInGroup = false) {
  const card = document.createElement('div');
  card.className = 'kiniela-person-card';
  card.setAttribute('draggable', 'true');
  card.setAttribute('data-id', member.id);
  card.setAttribute('data-is-new', member.isNewCap ? 'true' : 'false');

  if (member.isNewCap) {
    card.style.borderLeft = '4px solid var(--retro-orange)';
  }

  // Name Label
  const nameSpan = document.createElement('span');
  nameSpan.className = 'person-name';
  nameSpan.textContent = member.name;
  if (member.isNewCap) {
    nameSpan.innerHTML = `${escapeHTML(member.name)} <span style="font-size:0.7rem; background:#FFF7ED; color:var(--retro-orange); padding:1px 5px; border-radius:4px; margin-left:4px; font-weight:800;">TRUK</span>`;
  }
  card.appendChild(nameSpan);

  // Drag handlers
  card.addEventListener('dragstart', (e) => {
    e.dataTransfer.setData('text/plain', String(member.id));
    card.classList.add('dragging');
  });

  card.addEventListener('dragend', () => {
    card.classList.remove('dragging');
  });

  return card;
}

/* ==========================================================================
   DRAG & DROP ENGINE & RULES VALIDATION
   ========================================================================== */

function handleDragOver(e) {
  e.preventDefault();
  e.currentTarget.classList.add('drag-over');
}

function handleDragLeave(e) {
  e.currentTarget.classList.remove('drag-over');
}

function handleDrop(e, targetGroupCode) {
  e.preventDefault();
  e.currentTarget.classList.remove('drag-over');

  const rawId = e.dataTransfer.getData('text/plain');
  const memberId = Number(rawId);
  if (!Number.isInteger(memberId)) return;

  const member = MEMBERS_POOL.find(m => m.id === memberId);
  if (!member) return;

  assignMember(memberId, targetGroupCode);
}

function assignMember(memberId, groupCode) {
  assignments[memberId] = groupCode;
  renderPoolUI();
  renderGroupsUI();
}

/* ==========================================================================
   RANDOMIZER ENGINE & RESET
   ========================================================================== */

function randomizeKiniela() {
  resetAssignments();

  const allGroupCodes = GROUPS.map(g => g.code);
  const groupCounts = Object.fromEntries(allGroupCodes.map(c => [c, 0]));

  const shuffledPool = [...MEMBERS_POOL].sort(() => Math.random() - 0.5);

  // 1. Distribute Truks across all groups
  const truks = shuffledPool.filter(m => m.isNewCap);
  truks.forEach(truk => {
    // Pick the group with fewest members so far
    const sortedUnits = [...allGroupCodes].sort((a, b) => groupCounts[a] - groupCounts[b]);
    const chosenUnit = sortedUnits[0];
    assignments[truk.id] = chosenUnit;
    groupCounts[chosenUnit] += 1;
  });

  // 2. Ensure Marxen gets at least 3 experienced caps
  const experienced = shuffledPool.filter(m => !m.isNewCap);
  const marxenCaps = experienced.slice(0, 3);
  marxenCaps.forEach(cap => {
    assignments[cap.id] = 'marxen';
    groupCounts['marxen'] += 1;
  });

  // 3. Distribute remaining experienced caps evenly across all groups
  const remainingCaps = experienced.slice(3);
  remainingCaps.forEach(cap => {
    const sortedUnits = [...allGroupCodes].sort((a, b) => groupCounts[a] - groupCounts[b]);
    const chosenUnit = sortedUnits[0];
    assignments[cap.id] = chosenUnit;
    groupCounts[chosenUnit] += 1;
  });

  renderPoolUI();
  renderGroupsUI();
}

function resetKiniela() {
  if (confirm("Segur que vols reiniciar totes les assignacions i tornar-les a la llista?")) {
    resetAssignments();
    renderPoolUI();
    renderGroupsUI();
  }
}

/* ==========================================================================
   PUBLISH MODAL & SUBMISSION TO BACKEND
   ========================================================================== */

function openPublishModal() {
  const modal = document.getElementById('kiniela-publish-modal');
  if (!modal) return;

  const total = MEMBERS_POOL.length;
  const assigned = Object.values(assignments).filter(g => g !== 'pool').length;
  const unassigned = total - assigned;

  const summaryText = document.getElementById('kiniela-publish-summary-text');
  if (summaryText) summaryText.textContent = `Assignats: ${assigned} de ${total} caps (${Math.round((assigned / total) * 100)}%)`;

  const incompleteAlert = document.getElementById('kiniela-incomplete-alert');
  const unassignedNum = document.getElementById('kiniela-unassigned-num');
  if (incompleteAlert && unassignedNum) {
    if (unassigned > 0) {
      unassignedNum.textContent = unassigned;
      incompleteAlert.style.display = 'block';
    } else {
      incompleteAlert.style.display = 'none';
    }
  }

  const errEl = document.getElementById('kiniela-publish-error');
  if (errEl) errEl.style.display = 'none';

  modal.style.display = 'flex';
  modal.classList.add('active');

  setTimeout(() => {
    const input = document.getElementById('kiniela-creator-name');
    if (input) input.focus();
  }, 100);
}

function closePublishModal() {
  const modal = document.getElementById('kiniela-publish-modal');
  if (modal) {
    modal.style.display = 'none';
    modal.classList.remove('active');
  }
}

async function submitKinielaData() {
  const input = document.getElementById('kiniela-creator-name');
  const hpInput = document.getElementById('kiniela-hp');
  const submitBtn = document.getElementById('btn-confirm-publish');
  const errEl = document.getElementById('kiniela-publish-error');

  const creatorName = (input ? input.value : '').trim();
  if (!creatorName) {
    if (errEl) {
      errEl.textContent = "Si us plau, escriu el teu nom abans d'enviar la quiniela.";
      errEl.style.display = 'block';
    }
    if (input) input.focus();
    return;
  }

  // Format assignments by group name
  const formattedKiniela = {};
  GROUPS.forEach(g => {
    formattedKiniela[g.name] = MEMBERS_POOL
      .filter(m => assignments[m.id] === g.code)
      .map(m => m.name);
  });

  const payload = {
    creator_name: creatorName,
    assignments: formattedKiniela,
    hp: hpInput ? hpInput.value : ''
  };

  try {
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.textContent = "ENVIANT...";
    }
    if (errEl) errEl.style.display = 'none';

    const response = await fetch('/api/kiniela/save', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });

    const result = await response.json();

    if (!response.ok || result.status !== 'success') {
      throw new Error(result.message || "Error en desar la quiniela.");
    }

    closePublishModal();
    openSuccessModal(creatorName, result, formattedKiniela);

  } catch (err) {
    console.error("Error enviant la Quiniela:", err);
    if (errEl) {
      errEl.textContent = err.message || "Hi ha hagut un error en enviar la Quiniela. Torna-ho a provar.";
      errEl.style.display = 'block';
    }
  } finally {
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.textContent = "CONFIRMAR I ENVIAR";
    }
  }
}

function openSuccessModal(creatorName, result, formattedKiniela) {
  const modal = document.getElementById('kiniela-success-modal');
  if (!modal) return;

  const creatorInfo = document.getElementById('success-creator-info');
  if (creatorInfo) {
    creatorInfo.textContent = `Creador/a: ${creatorName.toUpperCase()} • Registrat: ${result.timestamp || ''} (Ref #${result.id || ''})`;
  }

  let summary = `QUINIELA DE CAPS 2026-2027\nCREADOR/A: ${creatorName.toUpperCase()}\nDATA: ${result.timestamp || ''}\n========================================\n`;
  GROUPS.forEach(g => {
    const list = formattedKiniela[g.name] || [];
    summary += `\n${g.name.toUpperCase()} (${list.length}):\n`;
    if (list.length > 0) {
      list.forEach(name => {
        summary += `  • ${name}\n`;
      });
    } else {
      summary += `  (Cap membre assignat)\n`;
    }
  });

  const textarea = document.getElementById('success-summary-textarea');
  if (textarea) textarea.value = summary;

  modal.style.display = 'flex';
  modal.classList.add('active');
}

function closeSuccessModal() {
  const modal = document.getElementById('kiniela-success-modal');
  if (modal) {
    modal.style.display = 'none';
    modal.classList.remove('active');
  }
}

/* ==========================================================================
   EVENT LISTENERS & BINDINGS
   ========================================================================== */

function setupActionButtons() {
  const btnRandom = document.getElementById('btn-random-kiniela');
  if (btnRandom) btnRandom.addEventListener('click', randomizeKiniela);

  const btnReset = document.getElementById('btn-reset-kiniela');
  if (btnReset) btnReset.addEventListener('click', resetKiniela);

  const btnPublish = document.getElementById('btn-publish-kiniela');
  if (btnPublish) btnPublish.addEventListener('click', openPublishModal);

  // Publish Modal Closes
  const btnClosePublish = document.getElementById('btn-close-publish-modal');
  if (btnClosePublish) btnClosePublish.addEventListener('click', closePublishModal);

  const btnCancelPublish = document.getElementById('btn-cancel-publish');
  if (btnCancelPublish) btnCancelPublish.addEventListener('click', closePublishModal);

  // Success Modal
  const btnCloseSuccess = document.getElementById('btn-close-success-modal');
  if (btnCloseSuccess) btnCloseSuccess.addEventListener('click', closeSuccessModal);

  const btnDoneSuccess = document.getElementById('btn-done-success');
  if (btnDoneSuccess) btnDoneSuccess.addEventListener('click', closeSuccessModal);

  const btnCopySummary = document.getElementById('btn-copy-summary');
  if (btnCopySummary) {
    btnCopySummary.addEventListener('click', () => {
      const textarea = document.getElementById('success-summary-textarea');
      if (textarea) {
        textarea.select();
        navigator.clipboard.writeText(textarea.value).then(() => {
          const orig = btnCopySummary.textContent;
          btnCopySummary.textContent = "✓ COPIAT!";
          setTimeout(() => { btnCopySummary.textContent = orig; }, 1800);
        }).catch(() => {
          alert("Resum copiat correctament!");
        });
      }
    });
  }

  // Backdrop clicks
  ['kiniela-publish-modal', 'kiniela-success-modal'].forEach(id => {
    const modal = document.getElementById(id);
    if (modal) {
      modal.addEventListener('click', (e) => {
        if (e.target === modal) {
          modal.style.display = 'none';
          modal.classList.remove('active');
        }
      });
    }
  });

  // ESC key closes modals
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closePublishModal();
      closeSuccessModal();
    }
  });
}

function setupSearchFilter() {
  const searchInput = document.getElementById('pool-search-input');
  if (searchInput) {
    searchInput.addEventListener('input', () => {
      renderPoolUI();
    });
  }
}

function escapeHTML(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
