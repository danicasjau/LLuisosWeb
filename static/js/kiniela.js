/**
 * AE LLUÏSOS DE GRÀCIA - KINIELA ESCOLTA ENGINE
 * Separated JavaScript file for Kiniela group assignment game & Google Sheets DB integration
 */

document.addEventListener('DOMContentLoaded', () => {
  console.log("⚡ Kiniela Escolta Engine Loaded");
  initKiniela();
});

// List of 22 Scout Members
const MEMBERS_POOL = [
  { id: 1, name: "Marc Vila", initials: "MV", photo: "/static/images/scout_team.jpg" },
  { id: 2, name: "Larraitz Echeverria", initials: "LE", photo: "/static/images/scout_team.jpg" },
  { id: 3, name: "Guillem Pujol", initials: "GP", photo: "/static/images/scout_team.jpg" },
  { id: 4, name: "Aina Fontcuberta", initials: "AF", photo: "/static/images/scout_team.jpg" },
  { id: 5, name: "Pol Serra", initials: "PS", photo: "/static/images/scout_team.jpg" },
  { id: 6, name: "Clara Rius", initials: "CR", photo: "/static/images/scout_team.jpg" },
  { id: 7, name: "Pau Soler", initials: "PS", photo: "/static/images/scout_team.jpg" },
  { id: 8, name: "Meritxell Balaguer", initials: "MB", photo: "/static/images/scout_team.jpg" },
  { id: 9, name: "Ignasi Mas", initials: "IM", photo: "/static/images/scout_team.jpg" },
  { id: 10, name: "Berta Canal", initials: "BC", photo: "/static/images/scout_team.jpg" },
  { id: 11, name: "Arnau Puig", initials: "AP", photo: "/static/images/scout_team.jpg" },
  { id: 12, name: "Laia Domènech", initials: "LD", photo: "/static/images/scout_team.jpg" },
  { id: 13, name: "Gerard Farré", initials: "GF", photo: "/static/images/scout_team.jpg" },
  { id: 14, name: "Mireia Rovira", initials: "MR", photo: "/static/images/scout_team.jpg" },
  { id: 15, name: "Oriol Noguera", initials: "ON", photo: "/static/images/scout_team.jpg" },
  { id: 16, name: "Judit Camps", initials: "JC", photo: "/static/images/scout_team.jpg" },
  { id: 17, name: "Xavi Vidal", initials: "XV", photo: "/static/images/scout_team.jpg" },
  { id: 18, name: "Núria Comas", initials: "NC", photo: "/static/images/scout_team.jpg" },
  { id: 19, name: "Ferran Dalmau", initials: "FD", photo: "/static/images/scout_team.jpg" },
  { id: 20, name: "Eulàlia Costa", initials: "EC", photo: "/static/images/scout_team.jpg" },
  { id: 21, name: "Bernat Badia", initials: "BB", photo: "/static/images/scout_team.jpg" },
  { id: 22, name: "Gemma Fortuny", initials: "GF", photo: "/static/images/scout_team.jpg" }
];

// Five units plus Marxen for people who leave the active units.
const GROUPS = [
  { code: "castors", name: "Castúdrigues", color: "#FF7A00" },
  { code: "llops", name: "Dainops", color: "#FFD21F" },
  { code: "ranguis", name: "Ranguis", color: "#2563EB" },
  { code: "pios", name: "Pionel·les", color: "#DC2626" },
  { code: "truk", name: "Truk", color: "#16A34A" },
  { code: "marxen", name: "Marxen", color: "#7C3AED" }
];

const NEW_CAPS = [
  { id: 1001, name: "Pau Nuet", isNewCap: true },
  { id: 1002, name: "Joan Nuet", isNewCap: true },
  { id: 1003, name: "Jana Bosc", isNewCap: true },
  { id: 1004, name: "Iris de Cook", isNewCap: true },
  { id: 1005, name: "Aniol Rovira", isNewCap: true },
  { id: 1006, name: "Júlia Muntada", isNewCap: true }
];

// State Management: memberId -> groupCode (or 'pool')
let assignments = {};

function initKiniela() {
  if (Array.isArray(window.CAPS_POOL) && window.CAPS_POOL.length > 0) {
    MEMBERS_POOL.length = 0;
    window.CAPS_POOL.forEach(member => {
      MEMBERS_POOL.push({
        id: member.id,
        name: member.name,
        photo: member.image,
        role: member.role || '',
        unit: member.unit || '',
        years: member.years || '',
        bio: member.bio || '',
        quote: member.quote || ''
      });
    });
  }
  NEW_CAPS.forEach(member => MEMBERS_POOL.push(member));
  resetAssignments();
  renderGroupsUI();
  renderPoolUI();
  setupEventListeners();
  updateProgressUI();
}

function resetAssignments() {
  assignments = {};
  MEMBERS_POOL.forEach(m => {
    assignments[m.id] = 'pool';
  });
}

/* ==========================================================================
   UI RENDERING
   ========================================================================== */

function renderPoolUI() {
  const poolContainer = document.getElementById('unassigned-pool');
  if (!poolContainer) return;

  if (!poolContainer.dataset.dropReady) {
    poolContainer.addEventListener('dragover', handleDragOver);
    poolContainer.addEventListener('dragleave', handleDragLeave);
    poolContainer.addEventListener('drop', (e) => handleDrop(e, 'pool'));
    poolContainer.dataset.dropReady = 'true';
  }

  poolContainer.innerHTML = '';

  const unassigned = MEMBERS_POOL.filter(m => assignments[m.id] === 'pool');

  if (unassigned.length === 0) {
    poolContainer.innerHTML = `<div class="empty-pool-msg">Tots els membres estan assignats!</div>`;
    return;
  }

  const existingCaps = unassigned.filter(member => !member.isNewCap);
  const newCaps = unassigned.filter(member => member.isNewCap);

  existingCaps.forEach(member => {
    const card = createMemberCard(member);
    poolContainer.appendChild(card);
  });

  if (newCaps.length > 0) {
    const title = document.createElement('div');
    title.className = 'kiniela-new-caps-title';
    title.textContent = 'Nous Caps';
    poolContainer.appendChild(title);

    newCaps.forEach(member => {
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
      <div class="group-header" style="background-color: ${group.color};">
        <div class="group-title">${group.name}</div>
      </div>
      <div class="group-dropzone" data-group="${group.code}">
      </div>
    `;

    const dropzone = groupCol.querySelector('.group-dropzone');

    dropzone.addEventListener('dragover', handleDragOver);
    dropzone.addEventListener('dragleave', handleDragLeave);
    dropzone.addEventListener('drop', (e) => handleDrop(e, group.code));

    membersInGroup.forEach(member => {
      const card = createMemberCard(member);
      dropzone.appendChild(card);
    });

    groupsContainer.appendChild(groupCol);
  });
}

function createMemberCard(member) {
  const card = document.createElement('div');
  card.className = 'kiniela-person-card';
  card.setAttribute('draggable', 'true');
  card.setAttribute('data-id', member.id);

  card.innerHTML = `<span class="person-name">${member.name}</span>`;

  if (!member.isNewCap) card.addEventListener('click', () => {
    const modal = document.getElementById('retro-modal');
    const profileQuestions = `
      <div class="person-profile-questions">
        <p><strong>Nom i Cognoms:</strong> ${member.name}</p>
        <p><strong>Cap de:</strong> ${member.role}</p>
        <p><strong>Data de naixement:</strong></p>
        <p><strong>Any que va entrar al Cau:</strong></p>
        <p><strong>Estudis:</strong></p>
        <p><strong>Hobbies:</strong></p>
        <p><strong>Cançó preferida:</strong></p>
        <p><strong>Llibre preferit:</strong></p>
        <p><strong>Color preferit:</strong></p>
        <p><strong>Anècdota:</strong></p>
      </div>
    `;

    modal.classList.add('caps-person-modal');
    openModal(member.name, '', '', profileQuestions, member.photo);
  });

  card.addEventListener('dragstart', (e) => {
    e.dataTransfer.setData('text/plain', member.id);
    card.classList.add('dragging');
  });

  card.addEventListener('dragend', () => {
    card.classList.remove('dragging');
  });

  return card;
}

/* ==========================================================================
   DRAG & DROP HANDLERS
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

  const memberId = Number(e.dataTransfer.getData('text/plain'));
  if (Number.isInteger(memberId)) {
    const member = MEMBERS_POOL.find(candidate => candidate.id === memberId);
    if (member?.isNewCap && targetGroupCode === 'marxen') {
      showMarxenRestrictionMessage(e.currentTarget);
      return;
    }
    assignMember(memberId, targetGroupCode);
  }
}

function showMarxenRestrictionMessage(dropzone) {
  const existingMessage = dropzone.querySelector('.marxen-restriction-message');
  if (existingMessage) existingMessage.remove();

  const message = document.createElement('div');
  message.className = 'marxen-restriction-message';
  message.textContent = 'No es pot posar perquè és un nou cap';
  dropzone.appendChild(message);

  setTimeout(() => {
    message.remove();
  }, 1800);
}

/* ==========================================================================
   ASSIGNMENT ACTIONS & RANDOMIZER
   ========================================================================== */

function assignMember(memberId, groupCode) {
  assignments[memberId] = groupCode;
  renderPoolUI();
  renderGroupsUI();
  updateProgressUI();
}

function randomizeKiniela() {
  resetAssignments();
  const activeGroupCodes = GROUPS
    .filter(group => group.code !== 'marxen')
    .map(group => group.code);
  const allGroupCodes = [...activeGroupCodes, 'marxen'];
  const groupCounts = Object.fromEntries(allGroupCodes.map(groupCode => [groupCode, 0]));
  const shuffledMembers = [...MEMBERS_POOL].sort(() => Math.random() - 0.5);
  const marxenCandidates = shuffledMembers.filter(member => !member.isNewCap);
  const marxenMembers = marxenCandidates.slice(0, 3);

  marxenMembers.forEach(member => {
    assignments[member.id] = 'marxen';
    groupCounts.marxen += 1;
  });

  activeGroupCodes.forEach(groupCode => {
    shuffledMembers
      .filter(member => assignments[member.id] === 'pool')
      .splice(0, 3)
      .forEach(member => {
        assignments[member.id] = groupCode;
        groupCounts[groupCode] += 1;
      });
  });

  shuffledMembers.forEach(member => {
    if (assignments[member.id] !== 'pool') return;
    const availableGroupCodes = allGroupCodes.filter(groupCode => {
      const marxenBlocked = member.isNewCap && groupCode === 'marxen';
      return !marxenBlocked && groupCounts[groupCode] < 5;
    });
    const randomGroup = availableGroupCodes[Math.floor(Math.random() * availableGroupCodes.length)];
    assignments[member.id] = randomGroup;
    groupCounts[randomGroup] += 1;
  });

  renderPoolUI();
  renderGroupsUI();
  updateProgressUI();
}

function resetKiniela() {
  resetAssignments();
  renderPoolUI();
  renderGroupsUI();
  updateProgressUI();
}

function updateProgressUI() {
  const total = MEMBERS_POOL.length;
  const assigned = Object.values(assignments).filter(g => g !== 'pool').length;

  const counterEl = document.getElementById('kiniela-progress-counter');
  if (counterEl) {
    counterEl.textContent = `${assigned} / ${total}`;
  }

  const fillEl = document.getElementById('kiniela-progress-fill');
  if (fillEl) {
    const percentage = Math.round((assigned / total) * 100);
    fillEl.style.width = `${percentage}%`;
  }

  const publishButton = document.getElementById('btn-publish-kiniela');
  if (publishButton) {
    const isComplete = assigned === total;
    publishButton.textContent = isComplete ? 'PUBLICAR QUINIELA' : 'ALEATORI';
  }
}

/* ==========================================================================
   CLICK QUICK MENU & SAVE TO GOOGLE SHEETS
   ========================================================================== */

function showQuickAssignMenu(member, targetCard) {
  let menu = document.getElementById('quick-assign-menu');
  if (menu) menu.remove();

  menu = document.createElement('div');
  menu.id = 'quick-assign-menu';
  menu.className = 'quick-assign-dropdown';

  let optionsHTML = `<div class="menu-title">Moure a:</div>`;
  optionsHTML += `<button data-code="pool">Sense assignar</button>`;

  GROUPS.forEach(g => {
    optionsHTML += `<button data-code="${g.code}">${g.name}</button>`;
  });

  menu.innerHTML = optionsHTML;

  const rect = targetCard.getBoundingClientRect();
  menu.style.top = `${window.scrollY + rect.bottom + 5}px`;
  menu.style.left = `${window.scrollX + rect.left}px`;

  document.body.appendChild(menu);

  menu.querySelectorAll('button').forEach(btn => {
    btn.addEventListener('click', () => {
      const code = btn.getAttribute('data-code');
      assignMember(member.id, code);
      menu.remove();
    });
  });

  const closeOnClickOutside = (e) => {
    if (!menu.contains(e.target) && e.target !== targetCard) {
      menu.remove();
      document.removeEventListener('click', closeOnClickOutside);
    }
  };
  setTimeout(() => document.addEventListener('click', closeOnClickOutside), 100);
}

function setupEventListeners() {
  const btnPublish = document.getElementById('btn-publish-kiniela');
  if (btnPublish) {
    btnPublish.addEventListener('click', () => {
      const assigned = Object.values(assignments).filter(group => group !== 'pool').length;
      const total = MEMBERS_POOL.length;
      if (assigned === total) {
        openPublishNameModal();
      } else {
        randomizeKiniela();
      }
    });
  }

  const btnReset = document.getElementById('btn-reset-kiniela');
  if (btnReset) btnReset.addEventListener('click', resetKiniela);
}

function openPublishNameModal() {
  const total = MEMBERS_POOL.length;
  const assigned = Object.values(assignments).filter(g => g !== 'pool').length;

  openModal(
    "PUBLICAR LA TEVA QUINIELA",
    "ENVIAR PROPOSTA",
    `Assignats ${assigned} de ${total} caps`,
    `
      <div style="margin-top: 5px; margin-bottom: 10px;">
        <label style="font-family: var(--font-display); font-size: 1rem; letter-spacing: 1px; display: block; margin-bottom: 10px; color: var(--ink-black);">
          INTRODUEIX EL TEU NOM COM A CREADOR/A:
        </label>
        <input type="text" id="modal-creator-name-input" class="creator-input" placeholder="El teu nom (ex: Maria, Pau, Marc...)" style="width: 100%; margin-bottom: 20px; font-size: 1rem; padding: 12px 16px;" autofocus />
        <button id="modal-submit-publish-btn" class="btn-retro btn-retro-orange" style="width: 100%; justify-content: center; padding: 14px 20px;">
          ENVIAR QUINIELA AL BACKEND
        </button>
      </div>
    `
  );

  setTimeout(() => {
    const inputEl = document.getElementById('modal-creator-name-input');
    const submitBtn = document.getElementById('modal-submit-publish-btn');

    if (inputEl) inputEl.focus();

    const handleSend = () => {
      const name = inputEl ? inputEl.value.trim() : '';
      if (!name) {
        alert("Si us plau, escriu el teu nom per publicar la Quiniela!");
        if (inputEl) inputEl.focus();
        return;
      }
      saveKinielaToDB(name);
    };

    if (submitBtn) {
      submitBtn.addEventListener('click', handleSend);
    }

    if (inputEl) {
      inputEl.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') handleSend();
      });
    }
  }, 120);
}

async function saveKinielaToDB(creatorName) {
  if (!creatorName) {
    creatorName = "Anònim/a Escolta";
  }

  const formattedKiniela = {};
  GROUPS.forEach(g => {
    formattedKiniela[g.name] = MEMBERS_POOL
      .filter(m => assignments[m.id] === g.code)
      .map(m => m.name);
  });

  try {
    const response = await fetch('/api/kiniela/save', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        creator_name: creatorName,
        assignments: formattedKiniela
      })
    });

    const result = await response.json();

    let summary = `QUINIELA DE CAPS - CREADOR: ${creatorName.toUpperCase()}\n===================================\n`;
    GROUPS.forEach(g => {
      const names = formattedKiniela[g.name] || [];
      summary += `\n${g.name.toUpperCase()}:\n`;
      if (names.length > 0) {
        names.forEach(n => summary += `  - ${n}\n`);
      } else {
        summary += `  (Cap membre assignat)\n`;
      }
    });

    openModal("QUINIELA PUBLICADA AMB ÈXIT! 🎉", "GOOGLE SHEETS DB", `Creador: ${creatorName} • ${result.timestamp || ''}`, `
      <div style="background:#DCFCE7; border:1px solid #166534; padding:12px; color:#14532D; font-weight:bold; margin-bottom:15px; border-radius:8px;">
        ${result.message || 'Quiniela registrada correctament!'}
      </div>
      <p style="margin-bottom:10px; font-weight:bold;">Resum enviat:</p>
      <textarea style="width:100%; height:180px; font-family:monospace; padding:10px; border:1px solid var(--border-dark); font-size:0.85rem; border-radius:8px;" readonly>${summary}</textarea>
    `);
  } catch (err) {
    console.error("Error saving Quiniela:", err);
    alert("Hi ha hagut un error en guardar la Quiniela. Torna-ho a intentar.");
  }
}
