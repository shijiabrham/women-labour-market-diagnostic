/**
 * ==============================================================================
 * Women's Labour Market Diagnostic in India — Static Application Logic (app.js)
 * Fully faithful to the Phase 9 Gradio implementation and Phase 1-8 outputs.
 * ==============================================================================
 */

// Global State Cache
const STATE = {
  tab1: null,
  tab2: null,
  tab3: null,
  tab4: null,
  tab5: null,
  tab6: null,
  activeTab: 'tab1'
};

// UI Helpers
function renderKpiCard(title, value, subtext = '', badge = '') {
  const badgeHtml = badge
    ? `<span class="kpi-badge">${badge}</span>`
    : '';
  return `
    <div class="kpi-card">
      <div class="kpi-header">
        <span class="kpi-title">${title}</span>
        ${badgeHtml}
      </div>
      <div class="kpi-value">${value}</div>
      <div class="kpi-subtext">${subtext}</div>
    </div>
  `;
}

// ------------------------------------------------------------------------------
// TAB 1: National Diagnostic Overview (5 Integrated Evidence Themes)
// ------------------------------------------------------------------------------
function initTab1() {
  if (!STATE.tab1) return;
  const data = STATE.tab1;
  const te = data.theme_evidence || {};

  // Render Executive Metric Ribbon (4 Verified High-Value Metrics)
  renderTab1ExecutiveRibbon();

  // Setup Theme 1 (Macro Participation Divide)
  const t1IndRadios = document.querySelectorAll('input[name="tab1_t1_ind"]');
  function updateTheme1() {
    const selInd = document.querySelector('input[name="tab1_t1_ind"]:checked').value;
    t1IndRadios.forEach(r => r.parentElement.classList.toggle('active', r.checked));
    renderTab1ChartTheme1(selInd);
  }
  t1IndRadios.forEach(r => r.addEventListener('change', updateTheme1));
  updateTheme1();

  // Setup Theme 2 (Spatial Segmentation)
  const t2IndRadios = document.querySelectorAll('input[name="tab1_t2_ind"]');
  function updateTheme2() {
    const selInd = document.querySelector('input[name="tab1_t2_ind"]:checked').value;
    t2IndRadios.forEach(r => r.parentElement.classList.toggle('active', r.checked));
    renderTab1ChartTheme2(selInd);
  }
  t2IndRadios.forEach(r => r.addEventListener('change', updateTheme2));
  updateTheme2();

  // Setup Theme 3 (Educational U-Curve)
  const t3ViewRadios = document.querySelectorAll('input[name="tab1_t3_view"]');
  function updateTheme3() {
    const selView = document.querySelector('input[name="tab1_t3_view"]:checked').value;
    t3ViewRadios.forEach(r => r.parentElement.classList.toggle('active', r.checked));
    renderTab1ChartTheme3(selView);
  }
  t3ViewRadios.forEach(r => r.addEventListener('change', updateTheme3));
  updateTheme3();

  // Setup Theme 4 (Educated Unemployment by Year)
  const t4YearRadios = document.querySelectorAll('input[name="tab1_t4_year"]');
  function updateTheme4() {
    const selYear = document.querySelector('input[name="tab1_t4_year"]:checked').value;
    t4YearRadios.forEach(r => r.parentElement.classList.toggle('active', r.checked));
    renderTab1Theme4(selYear);
  }
  t4YearRadios.forEach(r => r.addEventListener('change', updateTheme4));
  updateTheme4();

  // Setup Theme 5 (Enterprise Structure by Year)
  const t5YearRadios = document.querySelectorAll('input[name="tab1_t5_year"]');
  function updateTheme5() {
    const selYear = document.querySelector('input[name="tab1_t5_year"]:checked').value;
    t5YearRadios.forEach(r => r.parentElement.classList.toggle('active', r.checked));
    renderTab1Theme5(selYear);
  }
  t5YearRadios.forEach(r => r.addEventListener('change', updateTheme5));

  // Setup Collapsible Statistical Evidence in Theme 5
  const statAccordion = document.getElementById('tab1-t5-stat-accordion');
  if (statAccordion) {
    const trigger = statAccordion.querySelector('.accordion-trigger');
    if (trigger && !trigger.hasAttribute('data-bound')) {
      trigger.setAttribute('data-bound', 'true');
      trigger.addEventListener('click', () => {
        statAccordion.classList.toggle('open');
      });
    }
  }

  updateTheme5();
}

function renderTab1ExecutiveRibbon() {
  const d = STATE.tab1;
  if (!d) return;

  const lfprKpis = d.indicators?.LFPR?.kpis || {};
  const f23 = lfprKpis.female_2023 !== undefined ? `${lfprKpis.female_2023.toFixed(1)}%` : '45.0%';
  const m23 = lfprKpis.male_2023 !== undefined ? `${lfprKpis.male_2023.toFixed(1)}%` : '78.1%';
  const gap23 = lfprKpis.gap_2023 !== undefined ? `${lfprKpis.gap_2023.toFixed(1)} pp` : '-33.1 pp';

  const c1 = renderKpiCard(
    'Gender Gap in LFPR (2023)',
    gap23,
    `Female: ${f23} vs. Male: ${m23} (Narrowed by +16.4 pp since 2017)`,
    'Unweighted Mean'
  );

  const c2 = renderKpiCard(
    'Rural–Urban Female LFPR Change',
    '+24.5 pp vs. +9.4 pp',
    'Rural rose to 51.0% | Urban rose to 31.2% (Gap widened to 19.8 pp)',
    'Finding F4'
  );

  const c3 = renderKpiCard(
    'Graduate Unemployment Gap (2023)',
    '+12.6 pp',
    'Female Graduates: 23.3% vs. Male Graduates: 10.7% (2.2× male rate)',
    'Finding F6'
  );

  const c4 = renderKpiCard(
    'Non-Farm Enterprise Distribution (2023)',
    '56.6% Proprietary',
    'Public Sector: 24.9% F vs 16.0% M | Domestic Work: 6.3% F vs 0.8% M',
    'Dataset 7131'
  );

  const ribbonEl = document.getElementById('tab1-kpi-ribbon');
  if (ribbonEl) ribbonEl.innerHTML = `${c1}${c2}${c3}${c4}`;
}

function renderTab1ChartTheme1(indicator) {
  const te = STATE.tab1.theme_evidence?.theme1;
  const indData = te?.indicators?.[indicator] || STATE.tab1.indicators?.[indicator];
  const years = te?.years || STATE.tab1.years;
  if (!indData) return;

  const traces = [
    {
      x: years,
      y: indData.female,
      name: `Female ${indicator}`,
      mode: 'lines+markers+text',
      line: { color: '#2563eb', width: 3 },
      marker: { size: 8, color: '#2563eb' },
      text: indData.female.map(v => v !== null ? `${v.toFixed(1)}%` : 'N/A'),
      textposition: 'top center'
    },
    {
      x: years,
      y: indData.male,
      name: `Male ${indicator}`,
      mode: 'lines+markers+text',
      line: { color: '#64748b', width: 2, dash: 'dot' },
      marker: { size: 6, color: '#64748b' },
      text: indData.male.map(v => v !== null ? `${v.toFixed(1)}%` : 'N/A'),
      textposition: 'top center'
    }
  ];

  const yRange = indicator === 'Unemployment_Rate' ? [0, 20] : [0, 100];
  const layout = {
    title: `National Trajectory: ${indicator} (2017–2023, Unweighted Analytical Mean)`,
    xaxis: { title: 'Survey Wave', dtick: 1 },
    yaxis: { title: `${indicator} (%) [Unweighted Mean]`, range: yRange },
    template: 'plotly_white',
    legend: { orientation: 'h', yanchor: 'bottom', y: 1.02, xanchor: 'right', x: 1 },
    margin: { l: 45, r: 30, t: 50, b: 40 },
    height: 380
  };

  Plotly.newPlot('tab1-chart-theme1', traces, layout, { responsive: true, displayModeBar: false });
}

function renderTab1ChartTheme2(indicator) {
  const te2 = STATE.tab1.theme_evidence?.theme2;
  if (!te2) return;
  const indData = te2[indicator];
  const years = te2.years;
  if (!indData) return;

  const traces = [
    {
      x: years,
      y: indData.female_rural,
      name: `Female Rural ${indicator}`,
      mode: 'lines+markers+text',
      line: { color: '#16a34a', width: 3 },
      marker: { size: 8, color: '#16a34a' },
      text: indData.female_rural.map(v => v !== null ? `${v.toFixed(1)}%` : 'N/A'),
      textposition: 'top center'
    },
    {
      x: years,
      y: indData.female_urban,
      name: `Female Urban ${indicator}`,
      mode: 'lines+markers+text',
      line: { color: '#2563eb', width: 3, dash: 'dot' },
      marker: { size: 8, color: '#2563eb' },
      text: indData.female_urban.map(v => v !== null ? `${v.toFixed(1)}%` : 'N/A'),
      textposition: 'bottom center'
    }
  ];

  const layout = {
    title: `Rural–Urban Divergence in Female ${indicator} (2017–2023)`,
    xaxis: { title: 'Survey Wave', dtick: 1 },
    yaxis: { title: `${indicator} (%) [Unweighted Mean]`, range: [0, 70] },
    template: 'plotly_white',
    legend: { orientation: 'h', yanchor: 'bottom', y: 1.02, xanchor: 'right', x: 1 },
    margin: { l: 45, r: 30, t: 50, b: 40 },
    height: 380
  };

  Plotly.newPlot('tab1-chart-theme2', traces, layout, { responsive: true, displayModeBar: false });
}

function formatEduLabel(label) {
  if (label === 'Diploma/ Certificate Course') return 'Diploma / Certificate';
  if (label === 'Post Graduate & Above') return 'Post Graduate & Above';
  if (label === 'Literate & Upto Primary') return 'Literate & Primary';
  return label;
}

function renderTab1ChartTheme3(viewMode) {
  const te3 = STATE.tab1.theme_evidence?.theme3;
  if (!te3) return;

  const displayEduLevels = te3.education_levels.map(formatEduLabel);
  let traces = [];
  let titleStr = '';
  let yAxisTitle = 'LFPR (%)';

  if (viewMode === '2023') {
    titleStr = 'The Education Gradient: LFPR by Attainment Tier (2023 Single-Year)';
    traces = [
      {
        x: displayEduLevels,
        y: te3.female_2023,
        name: 'Female LFPR (2023)',
        type: 'bar',
        marker: { color: '#2563eb' },
        text: te3.female_2023.map(v => v !== null ? `${v.toFixed(1)}%` : 'N/A'),
        textposition: 'outside'
      },
      {
        x: displayEduLevels,
        y: te3.male_2023,
        name: 'Male LFPR (2023)',
        type: 'bar',
        marker: { color: '#94a3b8' },
        text: te3.male_2023.map(v => v !== null ? `${v.toFixed(1)}%` : 'N/A'),
        textposition: 'outside'
      }
    ];
  } else if (viewMode === 'pooled') {
    titleStr = 'Multi-Year Baseline U-Curve: Education Gradient (2017–2023 Pooled Means)';
    traces = [
      {
        x: displayEduLevels,
        y: te3.female_pooled,
        name: 'Female LFPR (2017–2023 Pooled)',
        type: 'bar',
        marker: { color: '#1d4ed8' },
        text: te3.female_pooled.map(v => v !== null ? `${v.toFixed(1)}%` : 'N/A'),
        textposition: 'outside'
      },
      {
        x: displayEduLevels,
        y: te3.male_pooled,
        name: 'Male LFPR (2017–2023 Pooled)',
        type: 'bar',
        marker: { color: '#94a3b8' },
        text: te3.male_pooled.map(v => v !== null ? `${v.toFixed(1)}%` : 'N/A'),
        textposition: 'outside'
      }
    ];
  } else if (viewMode === 'gains') {
    titleStr = 'Disproportionate Low-Education LFPR Expansion (2017 → 2023 Net Gains, Finding F8)';
    yAxisTitle = 'Net Change (pp)';
    traces = [
      {
        x: displayEduLevels,
        y: te3.female_delta_f8,
        name: 'Female LFPR Net Gain (pp)',
        type: 'bar',
        marker: { color: '#16a34a' },
        text: te3.female_delta_f8.map(v => v !== null ? `+${v.toFixed(1)} pp` : 'N/A'),
        textposition: 'outside'
      }
    ];
  }

  const layout = {
    title: {
      text: titleStr,
      font: { size: 14 }
    },
    xaxis: {
      title: 'Educational Attainment',
      tickangle: -25,
      automargin: true
    },
    yaxis: {
      title: `${yAxisTitle} [Unweighted Mean]`,
      range: viewMode === 'gains' ? [0, 32] : [0, 100]
    },
    barmode: 'group',
    template: 'plotly_white',
    legend: {
      orientation: 'h',
      yanchor: 'bottom',
      y: 1.05,
      xanchor: 'right',
      x: 1
    },
    margin: { l: 50, r: 30, t: 75, b: 90 },
    height: 410
  };

  Plotly.newPlot('tab1-chart-theme3', traces, layout, { responsive: true, displayModeBar: false });
}

function renderTab1Theme4(year) {
  const te4 = STATE.tab1.theme_evidence?.theme4;
  if (!te4) return;

  const yrStr = String(year);
  const yrData = te4.data_by_year?.[yrStr] || {
    female: te4.female_2023,
    male: te4.male_2023,
    gender_gap: te4.gender_gap_2023
  };

  const displayEduLevels = te4.education_levels.map(formatEduLabel);
  const traces = [
    {
      x: displayEduLevels,
      y: yrData.female,
      name: `Female Unemployment Rate (${year})`,
      type: 'bar',
      marker: { color: '#e11d48' },
      text: yrData.female.map(v => v !== null ? `${v.toFixed(1)}%` : 'N/A'),
      textposition: 'outside'
    },
    {
      x: displayEduLevels,
      y: yrData.male,
      name: `Male Unemployment Rate (${year})`,
      type: 'bar',
      marker: { color: '#94a3b8' },
      text: yrData.male.map(v => v !== null ? `${v.toFixed(1)}%` : 'N/A'),
      textposition: 'outside'
    }
  ];

  const layout = {
    title: {
      text: `Educated Unemployment Penalty by Tier (${year}, Rural + Urban)`,
      font: { size: 14 }
    },
    xaxis: {
      title: 'Educational Attainment',
      tickangle: -25,
      automargin: true
    },
    yaxis: {
      title: 'Unemployment Rate (%) [Unweighted Mean]',
      range: [0, 36]
    },
    barmode: 'group',
    template: 'plotly_white',
    legend: {
      orientation: 'h',
      yanchor: 'bottom',
      y: 1.05,
      xanchor: 'right',
      x: 1
    },
    margin: { l: 50, r: 30, t: 75, b: 90 },
    height: 410
  };

  Plotly.newPlot('tab1-chart-theme4', traces, layout, { responsive: true, displayModeBar: false });

  // Update dynamic year-specific narrative figures
  const headerEl = document.getElementById('tab1-t4-evidence-header');
  const listEl = document.getElementById('tab1-t4-evidence-list');
  if (headerEl) headerEl.innerText = `Empirical Evidence & Statistical Support (${year}):`;

  if (listEl) {
    const fNotLit = yrData.female[0] !== null ? `${yrData.female[0].toFixed(1)}%` : 'N/A';
    const fPrim = yrData.female[1] !== null ? `${yrData.female[1].toFixed(1)}%` : 'N/A';
    const mNotLit = yrData.male[0] !== null ? `${yrData.male[0].toFixed(1)}%` : 'N/A';
    const mPrim = yrData.male[1] !== null ? `${yrData.male[1].toFixed(1)}%` : 'N/A';

    const fGrad = yrData.female[6] !== null ? `${yrData.female[6].toFixed(1)}%` : 'N/A';
    const mGrad = yrData.male[6] !== null ? `${yrData.male[6].toFixed(1)}%` : 'N/A';
    const gapGrad = yrData.gender_gap[6] !== null ? `${yrData.gender_gap[6] >= 0 ? '+' : ''}${yrData.gender_gap[6].toFixed(1)} percentage points` : 'N/A';
    const ratioGrad = (yrData.female[6] !== null && yrData.male[6] && yrData.male[6] > 0) ? ` (${(yrData.female[6] / yrData.male[6]).toFixed(1)}× male rate)` : '';

    const fPg = yrData.female[7] !== null ? `${yrData.female[7].toFixed(1)}%` : 'N/A';
    const mPg = yrData.male[7] !== null ? `${yrData.male[7].toFixed(1)}%` : 'N/A';
    const gapPg = yrData.gender_gap[7] !== null ? `${yrData.gender_gap[7] >= 0 ? '+' : ''}${yrData.gender_gap[7].toFixed(1)} percentage points` : 'N/A';

    listEl.innerHTML = `
      <li><strong>Low-Tier Unemployment:</strong> Open unemployment in ${year} was ${fNotLit} for non-literate women and ${fPrim} for primary-educated women, closely mirroring male rates of ${mNotLit} and ${mPrim}.</li>
      <li><strong>Graduate Friction:</strong> Female graduate unemployment was <strong>${fGrad}</strong> compared to <strong>${mGrad}</strong> for male graduates—representing a gender penalty of <strong>${gapGrad}</strong>${ratioGrad}.</li>
      <li><strong>Postgraduate Penalty:</strong> Postgraduate female unemployment reached <strong>${fPg}</strong> (vs. ${mPg} for men; gender penalty: <strong>${gapPg}</strong>).</li>
    `;
  }
}

function renderTab1Theme5(year) {
  const te5 = STATE.tab1.theme_evidence?.theme5;
  if (!te5) return;

  const yrStr = String(year);
  const yrData = te5.data_by_year?.[yrStr] || {
    female_shares: te5.female_shares,
    male_shares: te5.male_shares,
    gender_difference: te5.gender_difference
  };

  const traces = [
    {
      y: te5.enterprise_types,
      x: yrData.female_shares,
      orientation: 'h',
      name: `Female (% of Non-Farm Workers, ${year})`,
      type: 'bar',
      marker: { color: '#2563eb' },
      text: yrData.female_shares.map(v => v !== null ? `${v.toFixed(1)}%` : 'N/A'),
      textposition: 'outside',
      cliponaxis: false
    },
    {
      y: te5.enterprise_types,
      x: yrData.male_shares,
      orientation: 'h',
      name: `Male (% of Non-Farm Workers, ${year})`,
      type: 'bar',
      marker: { color: '#94a3b8' },
      text: yrData.male_shares.map(v => v !== null ? `${v.toFixed(1)}%` : 'N/A'),
      textposition: 'outside',
      cliponaxis: false
    }
  ];

  const layout = {
    title: {
      text: `Non-Agricultural Enterprise Distribution: NIC 05–99 (${year}, Rural + Urban)`,
      font: { size: 15, color: '#0f172a' },
      x: 0,
      xanchor: 'left'
    },
    xaxis: {
      title: 'Gender-Specific Distribution Across Enterprise Categories (%) [Unweighted Analytical Mean across 36 States/UTs, N=36]',
      range: [0, 80],
      automargin: true
    },
    yaxis: {
      title: '',
      automargin: true
    },
    barmode: 'group',
    template: 'plotly_white',
    legend: {
      orientation: 'h',
      yanchor: 'bottom',
      y: 1.08,
      xanchor: 'right',
      x: 1
    },
    margin: { l: 250, r: 40, t: 80, b: 65 },
    height: 440
  };

  Plotly.newPlot('tab1-chart-theme5', traces, layout, { responsive: true, displayModeBar: false });

  // Render Compact Key Finding Cards below chart
  renderTab1Theme5Cards(te5.enterprise_types, yrData, year);
}

function renderTab1Theme5Cards(entTypes, yrData, year) {
  const container = document.getElementById('tab1-t5-finding-cards');
  if (!container) return;

  const getVals = (name) => {
    const idx = entTypes.findIndex(t => t.toLowerCase().includes(name.toLowerCase()));
    if (idx === -1) return { f: 'N/A', m: 'N/A', diff: 'N/A', diffVal: 0 };
    const fVal = yrData.female_shares[idx];
    const mVal = yrData.male_shares[idx];
    const diffVal = yrData.gender_difference[idx];
    return {
      f: fVal !== null ? `${fVal.toFixed(1)}%` : 'N/A',
      m: mVal !== null ? `${mVal.toFixed(1)}%` : 'N/A',
      diff: diffVal !== null ? `${diffVal >= 0 ? '+' : ''}${diffVal.toFixed(1)} pp` : 'N/A',
      diffVal: diffVal !== null ? diffVal : 0
    };
  };

  const prop = getVals('proprietary');
  const govt = getVals('govt');
  const dom = getVals('household');
  const corp = getVals('limited company');

  container.innerHTML = `
    <div class="finding-card">
      <div class="finding-card-header">
        <span class="finding-card-title">Proprietary &amp; Partnership</span>
        <span class="finding-card-badge">${year}</span>
      </div>
      <div class="finding-card-row">
        <div class="finding-card-metric">
          <span class="finding-card-metric-label">Female</span>
          <span class="finding-card-metric-val">${prop.f}</span>
        </div>
        <div class="finding-card-metric">
          <span class="finding-card-metric-label">Male</span>
          <span class="finding-card-metric-val" style="color: #64748b;">${prop.m}</span>
        </div>
        <span class="finding-card-diff ${prop.diffVal >= 0 ? 'diff-positive' : 'diff-negative'}">${prop.diff}</span>
      </div>
      <div class="finding-card-statement">Primary non-farm absorber for both genders; men show a ${Math.abs(prop.diffVal).toFixed(1)} pp higher concentration.</div>
    </div>
    <div class="finding-card">
      <div class="finding-card-header">
        <span class="finding-card-title">Public Sector / Government</span>
        <span class="finding-card-badge">${year}</span>
      </div>
      <div class="finding-card-row">
        <div class="finding-card-metric">
          <span class="finding-card-metric-label">Female</span>
          <span class="finding-card-metric-val" style="color: #16a34a;">${govt.f}</span>
        </div>
        <div class="finding-card-metric">
          <span class="finding-card-metric-label">Male</span>
          <span class="finding-card-metric-val" style="color: #64748b;">${govt.m}</span>
        </div>
        <span class="finding-card-diff ${govt.diffVal >= 0 ? 'diff-positive' : 'diff-negative'}">${govt.diff}</span>
      </div>
      <div class="finding-card-statement">Female non-farm workers show a ${Math.abs(govt.diffVal).toFixed(1)} pp higher reliance on public sector jobs than men.</div>
    </div>
    <div class="finding-card">
      <div class="finding-card-header">
        <span class="finding-card-title">Employer Households (Domestic)</span>
        <span class="finding-card-badge">${year}</span>
      </div>
      <div class="finding-card-row">
        <div class="finding-card-metric">
          <span class="finding-card-metric-label">Female</span>
          <span class="finding-card-metric-val" style="color: #d97706;">${dom.f}</span>
        </div>
        <div class="finding-card-metric">
          <span class="finding-card-metric-label">Male</span>
          <span class="finding-card-metric-val" style="color: #64748b;">${dom.m}</span>
        </div>
        <span class="finding-card-diff ${dom.diffVal >= 0 ? 'diff-positive' : 'diff-negative'}">${dom.diff}</span>
      </div>
      <div class="finding-card-statement">Absorbs ${dom.f} of female non-farm workers, but is virtually absent (${dom.m}) among working men.</div>
    </div>
    <div class="finding-card">
      <div class="finding-card-header">
        <span class="finding-card-title">Corporate Limited Companies</span>
        <span class="finding-card-badge">${year}</span>
      </div>
      <div class="finding-card-row">
        <div class="finding-card-metric">
          <span class="finding-card-metric-label">Female</span>
          <span class="finding-card-metric-val" style="color: #475569;">${corp.f}</span>
        </div>
        <div class="finding-card-metric">
          <span class="finding-card-metric-label">Male</span>
          <span class="finding-card-metric-val" style="color: #64748b;">${corp.m}</span>
        </div>
        <span class="finding-card-diff ${corp.diffVal >= 0 ? 'diff-positive' : 'diff-negative'}">${corp.diff}</span>
      </div>
      <div class="finding-card-statement">Corporate enterprises absorb only a minor share; female employment lags male participation by ${Math.abs(corp.diffVal).toFixed(1)} pp.</div>
    </div>
  `;

  // Render Enterprise Structure Interpretation Section below cards
  const interpEl = document.getElementById('tab1-t5-interpretation');
  if (interpEl) {
    const propDiffText = prop.diffVal < 0 ? `${Math.abs(prop.diffVal).toFixed(1)} percentage points higher for men` : `${prop.diffVal.toFixed(1)} pp`;
    const govtDiffText = govt.diffVal > 0 ? `${govt.diffVal.toFixed(1)} percentage points higher for women` : `${govt.diffVal.toFixed(1)} pp`;
    const domDiffText = dom.diffVal > 0 ? `${dom.diffVal.toFixed(1)} percentage points higher for women` : `${dom.diffVal.toFixed(1)} pp`;
    const corpDiffText = corp.diffVal < 0 ? `${Math.abs(corp.diffVal).toFixed(1)} percentage points lower for women` : `${corp.diffVal.toFixed(1)} pp`;

    interpEl.innerHTML = `
      <h4>🏢 Enterprise Structure Interpretation (${year})</h4>
      <p><strong>Informal Concentration in Proprietary Enterprises:</strong> In ${year}, proprietary and partnership units constituted the primary non-agricultural employer for both genders, absorbing ${prop.f} of working women and ${prop.m} of working men. While predominant across both groups, concentration in proprietary units was ${propDiffText}, leaving the remaining female workforce structured around alternative destinations.</p>
      <p><strong>Disproportionate Public-Sector Anchor:</strong> Female non-agricultural employment exhibits a substantial relative reliance on government, local body, and public-sector enterprises (${govt.f} for women vs. ${govt.m} for men; ${govtDiffText}). The public sector operates as the foremost formal institution providing stable wage employment for non-farm women.</p>
      <p><strong>Contrasting Margins: Domestic Work vs. Corporate Absorption:</strong> Divergence is particularly marked across peripheral enterprise segments. Private employer households (domestic service) absorbed ${dom.f} of female non-farm workers compared to just ${dom.m} of men (${domDiffText}). In contrast, corporate structures (public and private limited companies) employed only ${corp.f} of working women compared to ${corp.m} of working men (${corpDiffText}), confirming limited female absorption into the formal corporate economy.</p>
      <p style="font-size: 12px; color: var(--slate-600); margin-top: 10px; border-top: 1px solid var(--slate-200); padding-top: 8px;"><em>Descriptive Analytical Boundary:</em> These cross-sectional findings capture observational distributions of employment across enterprise categories in the ${year} PLFS survey round (N = 36 States/UTs). They document structural compositional contrasts and do not establish causation or supply-side versus demand-side drivers.</p>
    `;
  }
}

// ------------------------------------------------------------------------------
// TAB 2: State Diagnostic Explorer
// ------------------------------------------------------------------------------
function initTab2() {
  if (!STATE.tab2) return;
  const data = STATE.tab2;

  // Populate Selectors
  const selA = document.getElementById('tab2-state-a');
  const selB = document.getElementById('tab2-state-b');
  const selYr = document.getElementById('tab2-year');

  selA.innerHTML = data.states.map(s => `<option value="${s}" ${s === 'Kerala' ? 'selected' : ''}>${s}</option>`).join('');
  selB.innerHTML = data.states.map(s => `<option value="${s}" ${s === 'Bihar' ? 'selected' : ''}>${s}</option>`).join('');
  selYr.innerHTML = data.years.map(y => `<option value="${y}" ${y === 2023 ? 'selected' : ''}>${y}</option>`).join('');

  // Event Listeners
  const indRadios = document.querySelectorAll('input[name="tab2_ind"]');
  const modeRadios = document.querySelectorAll('input[name="tab2_mode"]');

  function update() {
    const stA = selA.value;
    const stB = selB.value;
    const yr = parseInt(selYr.value, 10);
    const ind = document.querySelector('input[name="tab2_ind"]:checked').value;
    const mode = document.querySelector('input[name="tab2_mode"]:checked').value;

    indRadios.forEach(r => r.parentElement.classList.toggle('active', r.checked));
    modeRadios.forEach(r => r.parentElement.classList.toggle('active', r.checked));

    const bGroup = document.getElementById('tab2-state-b-group');
    bGroup.style.display = mode === 'Dual State Comparison' ? 'block' : 'none';

    renderTab2Badge(stA);
    renderTab2Kpis(stA, yr, ind);
    renderTab2Chart(stA, stB, yr, ind, mode);
    renderTab2Dossier(stA, yr, ind);
  }

  selA.addEventListener('change', update);
  selB.addEventListener('change', update);
  selYr.addEventListener('change', update);
  indRadios.forEach(r => r.addEventListener('change', update));
  modeRadios.forEach(r => r.addEventListener('change', update));

  update();
}

function renderTab2Badge(stateName) {
  const arch = STATE.tab2.archetypes[stateName] || STATE.tab2.default_archetype;
  document.getElementById('tab2-archetype-badge').innerHTML = `
    <div style="background:#f8fafc; border-left:4px solid #2563eb; padding:12px 16px; border-radius:4px; margin-bottom:14px;">
      <div style="font-size:14px; font-weight:700; color:#1e293b;">
        ${arch.icon} ${arch.name}
      </div>
      <div style="font-size:12px; color:#475569; margin-top:4px;">
        ${arch.desc}
      </div>
      <div style="font-size:11px; color:#94a3b8; margin-top:4px; font-style:italic;">
        Descriptive State-level labour-market archetype from Phase 8 synthesis (not a formal statistical cluster).
      </div>
    </div>
  `;
}

function renderTab2Kpis(stateName, year, indicator) {
  const curr = STATE.tab2.state_data[stateName]?.[year]?.[indicator];
  const base = STATE.tab2.state_data[stateName]?.[2017]?.[indicator];
  if (!curr) return;

  const fVal = curr.f_tot;
  const mVal = curr.m_tot;
  const gapVal = curr.gap;
  const fBaseVal = base ? base.f_tot : null;
  const delta = (fVal !== null && fBaseVal !== null) ? fVal - fBaseVal : null;

  const c1 = renderKpiCard(
    `${year} Female ${indicator}`,
    fVal !== null ? `${fVal.toFixed(1)}%` : 'N/A',
    delta !== null ? `${delta >= 0 ? '+' : ''}${delta.toFixed(1)} pp vs 2017 (${fBaseVal.toFixed(1)}%)` : 'No baseline comparison',
    `${stateName} Total`
  );
  const c2 = renderKpiCard(
    `${year} Gender Gap (F − M)`,
    gapVal !== null ? `${gapVal >= 0 ? '+' : ''}${gapVal.toFixed(1)} pp` : 'N/A',
    mVal !== null ? `Male Benchmark: ${mVal.toFixed(1)}%` : '',
    gapVal !== null && gapVal < 0 ? 'Disadvantage' : 'Benchmark'
  );
  const c3 = renderKpiCard(
    'Rural vs. Urban Female',
    curr.f_rural !== null && curr.f_urban !== null ? `${curr.f_rural.toFixed(1)}% / ${curr.f_urban.toFixed(1)}%` : 'N/A',
    curr.ru_gap !== null ? `Spatial Gap: ${curr.ru_gap >= 0 ? '+' : ''}${curr.ru_gap.toFixed(1)} pp (R − U)` : '',
    'Area Disparity'
  );

  document.getElementById('tab2-kpis').innerHTML = `${c1}${c2}${c3}`;
}

function renderTab2Chart(stA, stB, yr, ind, mode) {
  if (mode === 'Single State Trajectory') {
    const trends = STATE.tab2.state_data[stA]?.trends?.[ind];
    const years = STATE.tab2.years;
    if (!trends) return;

    const traces = [
      {
        x: years,
        y: trends.female,
        name: `Female ${ind}`,
        mode: 'lines+markers+text',
        line: { color: '#2563eb', width: 3 },
        marker: { size: 8, color: '#2563eb' },
        text: trends.female.map(v => v !== null ? `${v.toFixed(1)}%` : 'N/A'),
        textposition: 'top center'
      },
      {
        x: years,
        y: trends.male,
        name: `Male ${ind}`,
        mode: 'lines+markers+text',
        line: { color: '#64748b', width: 2, dash: 'dot' },
        marker: { size: 6, color: '#64748b' },
        text: trends.male.map(v => v !== null ? `${v.toFixed(1)}%` : 'N/A'),
        textposition: 'top center'
      }
    ];

    const yRange = ind === 'Unemployment_Rate' ? [0, 35] : [0, 100];
    const layout = {
      title: `${stA}: Temporal Trajectory of ${ind} (2017–2023)`,
      xaxis: { title: 'Survey Wave', dtick: 1 },
      yaxis: { title: `${ind} (%)`, range: yRange },
      template: 'plotly_white',
      legend: { orientation: 'h', yanchor: 'bottom', y: 1.02, xanchor: 'right', x: 1 },
      margin: { l: 40, r: 40, t: 60, b: 40 },
      height: 380
    };
    Plotly.newPlot('tab2-chart', traces, layout, { responsive: true, displayModeBar: false });
  } else {
    // DUAL STATE COMPARISON (Dumbbell Chart)
    const cat = ['Female Total', 'Male Total', 'Female Rural', 'Female Urban'];
    const getVals = st => {
      const d = STATE.tab2.state_data[st]?.[yr]?.[ind];
      return d ? [d.f_tot, d.m_tot, d.f_rural, d.f_urban] : [null, null, null, null];
    };
    const vA = getVals(stA);
    const vB = getVals(stB);

    const traces = [];
    cat.forEach((c, idx) => {
      if (vA[idx] !== null && vB[idx] !== null) {
        traces.push({
          x: [vA[idx], vB[idx]],
          y: [c, c],
          mode: 'lines',
          line: { color: '#94a3b8', width: 3 },
          showlegend: false
        });
      }
    });

    traces.push({
      x: vA,
      y: cat,
      mode: 'markers+text',
      name: `State A: ${stA}`,
      marker: { size: 14, color: '#2563eb' },
      text: vA.map(v => v !== null ? `${v.toFixed(1)}%` : 'N/A'),
      textposition: 'top center'
    });

    traces.push({
      x: vB,
      y: cat,
      mode: 'markers+text',
      name: `State B: ${stB}`,
      marker: { size: 14, color: '#e11d48' },
      text: vB.map(v => v !== null ? `${v.toFixed(1)}%` : 'N/A'),
      textposition: 'top center'
    });

    const layout = {
      title: `Dumbbell Comparison: ${stA} vs. ${stB} (${ind}, Year ${yr})`,
      xaxis: { title: `${ind} (%)` },
      yaxis: { title: 'Segment' },
      template: 'plotly_white',
      legend: { orientation: 'h', yanchor: 'bottom', y: 1.02, xanchor: 'right', x: 1 },
      margin: { l: 90, r: 40, t: 60, b: 40 },
      height: 380
    };
    Plotly.newPlot('tab2-chart', traces, layout, { responsive: true, displayModeBar: false });
  }
}

function renderTab2Dossier(stA, yr, ind) {
  const key = `${yr}_${ind}`;
  const dossier = STATE.tab2.state_dossiers[stA]?.[key] || [];
  let html = `<h3>📌 Deterministic State Dossier: ${stA}</h3>`;
  if (dossier.length > 0) {
    dossier.forEach(n => {
      html += `<p><strong>${n.headline || ''}</strong></p>`;
      html += `<p>${n.key_finding || ''}</p>`;
      if (n.change_statement) html += `<p>• <em>Change Statement:</em> ${n.change_statement}</p>`;
    });
  } else {
    html += `<p>In ${yr}, ${stA} exhibits key diagnostic patterns captured in PLFS Dataset 1.</p>`;
  }
  document.getElementById('tab2-dossier').innerHTML = html;
}

// ------------------------------------------------------------------------------
// TAB 3: Structural Fault Lines
// ------------------------------------------------------------------------------
function initTab3() {
  if (!STATE.tab3) return;
  const data = STATE.tab3;

  // Selectors
  const geoSel = document.getElementById('tab3-geography');
  const ucYearSel = document.getElementById('tab3-ucurve-year');
  const urYearSel = document.getElementById('tab3-ur-year');

  geoSel.innerHTML = data.geographies.map(g => `<option value="${g}">${g}</option>`).join('');
  ucYearSel.innerHTML = data.years.map(y => `<option value="${y}" ${y === 2023 ? 'selected' : ''}>${y}</option>`).join('');
  urYearSel.innerHTML = data.years.map(y => `<option value="${y}" ${y === 2023 ? 'selected' : ''}>${y}</option>`).join('');

  const ucAreaRadios = document.querySelectorAll('input[name="tab3_uc_area"]');
  const ruIndRadios = document.querySelectorAll('input[name="tab3_ru_ind"]');

  function updateUCurve() {
    const geo = geoSel.value;
    const area = document.querySelector('input[name="tab3_uc_area"]:checked').value;
    const yr = ucYearSel.value;
    ucAreaRadios.forEach(r => r.parentElement.classList.toggle('active', r.checked));

    const cur = data.data_by_geo[geo]?.u_curves[area]?.[yr];
    const noticeEl = document.getElementById('tab3-ucurve-notice');
    const bannerEl = document.getElementById('tab3-ucurve-method-banner');

    if (!cur || !cur.has_data) {
      noticeEl.style.display = 'block';
      noticeEl.className = 'warning-banner';
      noticeEl.innerHTML = `⚠️ <strong>Data Notice:</strong> In PLFS ${yr}, no rural survey observations were recorded for <strong>${geo}</strong> (classified as 100% urbanized). Values are not available and are NOT zero.`;

      if (bannerEl) {
        bannerEl.innerHTML = `<strong>State Educational Profile (${geo}, ${area}, ${yr}):</strong> No survey observations are recorded in PLFS microdata.<br><span style="font-size:12px; color:#64748b;"><em>All-India Benchmark Reference:</em> National female participation dips to a distinct trough at middle (30.2%) and secondary (23.7%) schooling tiers, rising only at technical diploma and postgraduate levels (Friedman χ² = 958.79, p < 0.001, ε² = 0.542).</span>`;
      }

      const layout = {
        title: `The Education Gradient: Labour Force Participation Rate (${geo}, ${area}, ${yr})`,
        template: 'plotly_white',
        height: 200,
        margin: { l: 40, r: 40, t: 40, b: 30 },
        annotations: [{
          text: `⚠️ No Survey Observations Available for ${geo} (${area}, ${yr})<br>Values are strictly missing / unrecorded and never imputed as zero.`,
          xref: 'paper', yref: 'paper',
          x: 0.5, y: 0.5, showarrow: false,
          font: { size: 13, color: '#b91c1c' }
        }],
        xaxis: { showgrid: false, zeroline: false, showticklabels: false },
        yaxis: { showgrid: false, zeroline: false, showticklabels: false }
      };
      Plotly.newPlot('tab3-ucurve-chart', [], layout, { responsive: true, displayModeBar: false });
      return;
    }

    noticeEl.style.display = 'none';

    // Update methodology banner dynamically based on geography
    if (bannerEl) {
      if (geo === 'All-India (Unweighted Mean)') {
        bannerEl.innerHTML = `<strong>Non-Monotone Education Gradient (All-India Benchmark):</strong> Across the 2017–2023 survey waves, the pooled analytical means show female labour-force participation dipping at middle schooling (30.2%) and secondary schooling (23.7%), before rising at technical diploma (56.6%) and postgraduate levels (59.1%) (Friedman χ² = 958.79, p < 0.001, ε² = 0.542). In the 2023 single-year view, the secondary-schooling trough persisted at 31.3%. These figures refer to different temporal scopes: the first set comprises pooled multi-year means, while the latter is a single-year observation.`;
      } else {
        const validPairs = data.education_levels
          .map((lvl, idx) => ({ lvl, val: cur.female[idx] }))
          .filter(p => p.val !== null);

        if (validPairs.length > 0) {
          const minP = validPairs.reduce((min, p) => p.val < min.val ? p : min, validPairs[0]);
          const maxP = validPairs.reduce((max, p) => p.val > max.val ? p : max, validPairs[0]);
          const midPair = validPairs.find(p => p.lvl.toLowerCase().includes('middle'));
          const secPair = validPairs.find(p => p.lvl.toLowerCase().includes('secondary') && !p.lvl.toLowerCase().includes('higher'));

          let midSecStr = '';
          if (midPair && secPair) {
            midSecStr = ` Middle schooling LFPR is ${midPair.val.toFixed(1)}% and secondary is ${secPair.val.toFixed(1)}%.`;
          }

          bannerEl.innerHTML = `<strong>State Educational Profile (${geo}, ${area}, ${yr}):</strong> Female LFPR reaches a minimum at <strong>${minP.lvl}</strong> (${minP.val.toFixed(1)}%) and peaks at <strong>${maxP.lvl}</strong> (${maxP.val.toFixed(1)}%).${midSecStr}<br><span style="font-size:12px; color:#64748b;"><em>All-India Benchmark Reference:</em> Across 2017–2023 pooled waves, national female participation dips to a distinct trough at middle (30.2%) and secondary (23.7%) schooling tiers, rising only at technical diploma (56.6%) and postgraduate levels (59.1%) (Friedman χ² = 958.79, p < 0.001, ε² = 0.542); in 2023, the secondary trough persisted at 31.3%.</span>`;
        } else {
          bannerEl.innerHTML = `<strong>State Educational Profile (${geo}, ${area}, ${yr}):</strong> No valid educational tier observations available.<br><span style="font-size:12px; color:#64748b;"><em>All-India Benchmark Reference:</em> Across 2017–2023 pooled waves, national female LFPR dips to middle (30.2%) and secondary (23.7%) tiers (Friedman χ² = 958.79, p < 0.001, ε² = 0.542); in 2023, the secondary trough persisted at 31.3%.</span>`;
        }
      }
    }

    const traces = [
      {
        x: data.education_levels,
        y: cur.female,
        name: 'Female LFPR',
        type: 'bar',
        marker: { color: '#2563eb' },
        text: cur.female.map(v => v !== null ? `${v.toFixed(1)}%` : 'N/A'),
        textposition: 'outside'
      },
      {
        x: data.education_levels,
        y: cur.male,
        name: 'Male LFPR',
        type: 'bar',
        marker: { color: '#94a3b8' },
        text: cur.male.map(v => v !== null ? `${v.toFixed(1)}%` : 'N/A'),
        textposition: 'outside'
      }
    ];

    const yTitle = (geo === 'All-India (Unweighted Mean)')
      ? 'LFPR (%) [Unweighted Analytical Mean]'
      : `LFPR (%) [${geo}]`;

    const layout = {
      title: `The Education Gradient: Labour Force Participation Rate by Education Tier (${geo}, ${area}, ${yr})`,
      xaxis: { title: 'Educational Attainment' },
      yaxis: { title: yTitle, range: [0, 100] },
      barmode: 'group',
      template: 'plotly_white',
      legend: { orientation: 'h', yanchor: 'bottom', y: 1.02, xanchor: 'right', x: 1 },
      margin: { l: 40, r: 40, t: 60, b: 100 },
      height: 420
    };
    Plotly.newPlot('tab3-ucurve-chart', traces, layout, { responsive: true, displayModeBar: false });
  }

  function updateUR() {
    const geo = geoSel.value;
    const yr = urYearSel.value;
    const cur = data.data_by_geo[geo]?.educated_unemployment[yr];
    const bannerEl = document.getElementById('tab3-ur-method-banner');

    if (!cur || !cur.has_data) {
      const layout = {
        title: `Educated Unemployment Penalty (${geo}, Rural + Urban, ${yr})`,
        template: 'plotly_white',
        height: 200,
        margin: { l: 40, r: 40, t: 40, b: 30 },
        annotations: [{
          text: `⚠️ No Survey Observations Available for ${geo} (${yr})<br>Values are strictly unrecorded and never imputed as zero.`,
          xref: 'paper', yref: 'paper',
          x: 0.5, y: 0.5, showarrow: false,
          font: { size: 13, color: '#b91c1c' }
        }],
        xaxis: { showgrid: false, zeroline: false, showticklabels: false },
        yaxis: { showgrid: false, zeroline: false, showticklabels: false }
      };
      Plotly.newPlot('tab3-ur-chart', [], layout, { responsive: true, displayModeBar: false });
      if (bannerEl) {
        bannerEl.innerHTML = `<strong>State Graduate Unemployment (${geo}, Rural + Urban, ${yr}):</strong> No survey observations available.<br><span style="font-size:12px; color:#64748b;"><em>All-India Benchmark Reference:</em> Nationally in 2023, graduate female unemployment was 23.3% (more than double the male graduate rate of 10.7%).</span>`;
      }
      return;
    }

    // Dynamic narrative update
    if (bannerEl) {
      if (geo === 'All-India (Unweighted Mean)') {
        bannerEl.innerHTML = `<strong>Extreme Graduate Friction (All-India Benchmark):</strong> While open unemployment is negligible for uneducated women, graduate female unemployment was 23.3% in 2023 (more than double the male graduate rate of 10.7%).`;
      } else {
        const gradIdx = data.education_levels.findIndex(l => l.toLowerCase().includes('graduate') && !l.toLowerCase().includes('post'));
        const fGrad = (gradIdx !== -1 && cur.female) ? cur.female[gradIdx] : null;
        const mGrad = (gradIdx !== -1 && cur.male) ? cur.male[gradIdx] : null;

        if (fGrad !== null && mGrad !== null) {
          const ratioText = (mGrad > 0) ? ` (${(fGrad / mGrad).toFixed(1)}× the male graduate rate)` : '';
          bannerEl.innerHTML = `<strong>State Graduate Unemployment (${geo}, Rural + Urban, ${yr}):</strong> Graduate female unemployment is <strong>${fGrad.toFixed(1)}%</strong> compared to <strong>${mGrad.toFixed(1)}%</strong> for male graduates${ratioText}.<br><span style="font-size:12px; color:#64748b;"><em>All-India Benchmark Reference:</em> Nationally in 2023, graduate female unemployment was 23.3% (more than double the male graduate rate of 10.7%).</span>`;
        } else {
          bannerEl.innerHTML = `<strong>State Graduate Unemployment (${geo}, Rural + Urban, ${yr}):</strong> Graduate observations are unavailable or sample is insufficient.<br><span style="font-size:12px; color:#64748b;"><em>All-India Benchmark Reference:</em> Nationally in 2023, graduate female unemployment was 23.3% (more than double the male graduate rate of 10.7%).</span>`;
        }
      }
    }

    const traces = [
      {
        x: data.education_levels,
        y: cur.female,
        name: 'Female Unemployment Rate',
        type: 'bar',
        marker: { color: '#e11d48' },
        text: cur.female.map(v => v !== null ? `${v.toFixed(1)}%` : 'N/A'),
        textposition: 'outside'
      },
      {
        x: data.education_levels,
        y: cur.male,
        name: 'Male Unemployment Rate',
        type: 'bar',
        marker: { color: '#94a3b8' },
        text: cur.male.map(v => v !== null ? `${v.toFixed(1)}%` : 'N/A'),
        textposition: 'outside'
      }
    ];

    const yTitle = (geo === 'All-India (Unweighted Mean)')
      ? 'Unemployment Rate (%) [Unweighted Mean]'
      : `Unemployment Rate (%) [${geo}]`;

    const layout = {
      title: `Educated Unemployment Penalty by Education Tier (${geo}, Rural + Urban, ${yr})`,
      xaxis: { title: 'Educational Attainment' },
      yaxis: { title: yTitle, range: [0, 35] },
      barmode: 'group',
      template: 'plotly_white',
      legend: { orientation: 'h', yanchor: 'bottom', y: 1.02, xanchor: 'right', x: 1 },
      margin: { l: 40, r: 40, t: 60, b: 100 },
      height: 420
    };
    Plotly.newPlot('tab3-ur-chart', traces, layout, { responsive: true, displayModeBar: false });
  }

  function updateRUDivergence() {
    const geo = geoSel.value;
    const ind = document.querySelector('input[name="tab3_ru_ind"]:checked').value;
    ruIndRadios.forEach(r => r.parentElement.classList.toggle('active', r.checked));

    const cur = data.data_by_geo[geo]?.rural_urban_divergence[ind];
    const bannerEl = document.getElementById('tab3-ru-method-banner');
    if (!cur) return;

    // Smart label positions: avoid overlapping text labels where rural and urban points are close
    const ruralPositions = [];
    const urbanPositions = [];
    data.years.forEach((_, i) => {
      const rVal = cur.female_rural[i];
      const uVal = cur.female_urban[i];
      if (rVal === null || uVal === null) {
        ruralPositions.push('top center');
        urbanPositions.push('top center');
      } else if (rVal >= uVal) {
        ruralPositions.push('top center');
        urbanPositions.push('bottom center');
      } else {
        ruralPositions.push('bottom center');
        urbanPositions.push('top center');
      }
    });

    const traces = [
      {
        x: data.years,
        y: cur.female_rural,
        name: `Female Rural ${ind}`,
        mode: 'lines+markers+text',
        line: { color: '#16a34a', width: 3 },
        marker: { size: 8, color: '#16a34a' },
        text: cur.female_rural.map(v => v !== null ? `${v.toFixed(1)}%` : ''),
        textposition: ruralPositions
      },
      {
        x: data.years,
        y: cur.female_urban,
        name: `Female Urban ${ind}`,
        mode: 'lines+markers+text',
        line: { color: '#2563eb', width: 3, dash: 'dot' },
        marker: { size: 8, color: '#2563eb' },
        text: cur.female_urban.map(v => v !== null ? `${v.toFixed(1)}%` : ''),
        textposition: urbanPositions
      }
    ];

    const yTitle = (geo === 'All-India (Unweighted Mean)')
      ? `${ind} (%) [Unweighted Mean]`
      : `${ind} (%) [${geo}]`;

    // Calculate sensible y-range with padding so top/bottom labels are never clipped
    const allVals = [...cur.female_rural, ...cur.female_urban].filter(v => v !== null);
    const maxVal = allVals.length > 0 ? Math.max(...allVals) : 60;
    const yMax = Math.max(70, Math.ceil((maxVal + 8) / 10) * 10);

    const layout = {
      title: `Rural-Urban Divergence in Female ${ind} (${geo}, 2017–2023)`,
      xaxis: { title: 'Survey Wave', dtick: 1 },
      yaxis: { title: yTitle, range: [0, yMax] },
      template: 'plotly_white',
      legend: { orientation: 'h', yanchor: 'bottom', y: 1.02, xanchor: 'right', x: 1 },
      margin: { l: 40, r: 40, t: 60, b: 40 },
      height: 380
    };
    Plotly.newPlot('tab3-ru-chart', traces, layout, { responsive: true, displayModeBar: false });

    // Update narrative banner dynamically
    if (bannerEl) {
      if (geo === 'All-India (Unweighted Mean)') {
        bannerEl.innerHTML = `<strong>Rural–Urban Divergence (All-India Analytical Benchmark):</strong> Across 36 States/UTs, unweighted rural female LFPR rose from 26.5% in 2017 to 51.0% in 2023 (+24.6 percentage points), while unweighted urban female LFPR rose from 21.7% to 31.2% (+9.5 percentage points). The rural–urban spatial gap widened from 4.7 percentage points in 2017 to 19.8 percentage points in 2023 (Finding F4: Wilcoxon W = 625.0, p < 0.001, r = 0.86).<br><span style="font-size:12px; color:#64748b;"><em>Official MoSPI population-weighted national estimates are different: rural female LFPR rose from 24.6% to 43.7%, while urban female LFPR rose from 20.4% to 25.4%.</em></span>`;
      } else {
        const r0 = cur.female_rural[0];
        const rEnd = cur.female_rural[cur.female_rural.length - 1];
        const u0 = cur.female_urban[0];
        const uEnd = cur.female_urban[cur.female_urban.length - 1];

        if (r0 !== null && rEnd !== null && u0 !== null && uEnd !== null) {
          const dR = rEnd - r0;
          const dU = uEnd - u0;
          const gap0 = r0 - u0;
          const gapEnd = rEnd - uEnd;
          bannerEl.innerHTML = `<strong>State Rural-Urban Trajectory (${geo}, ${ind}, 2017–2023):</strong> Rural female ${ind} moved from <strong>${r0.toFixed(1)}%</strong> to <strong>${rEnd.toFixed(1)}%</strong> (${dR >= 0 ? '+' : ''}${dR.toFixed(1)} pp), while urban female ${ind} moved from <strong>${u0.toFixed(1)}%</strong> to <strong>${uEnd.toFixed(1)}%</strong> (${dU >= 0 ? '+' : ''}${dU.toFixed(1)} pp). The rural–urban gap moved from ${gap0.toFixed(1)} pp to ${gapEnd.toFixed(1)} pp.<br><span style="font-size:12px; color:#64748b;"><em>All-India Benchmark Reference:</em> Across 36 States/UTs, unweighted female LFPR expansion was rural-led (+24.6 pp rural vs +9.5 pp urban), widening the spatial gap to 19.8 pp (Finding F4: Wilcoxon W = 625.0, p < 0.001, r = 0.86).</span>`;
        } else if (u0 !== null && uEnd !== null) {
          const dU = uEnd - u0;
          bannerEl.innerHTML = `<strong>State Rural-Urban Trajectory (${geo}, ${ind}, 2017–2023):</strong> Rural observations are unrecorded in recent waves (100% urbanized). Urban female ${ind} moved from <strong>${u0.toFixed(1)}%</strong> in 2017 to <strong>${uEnd.toFixed(1)}%</strong> in 2023 (${dU >= 0 ? '+' : ''}${dU.toFixed(1)} pp).<br><span style="font-size:12px; color:#64748b;"><em>All-India Benchmark Reference:</em> Across 36 States/UTs, unweighted female LFPR expansion was rural-led (+24.6 pp rural vs +9.5 pp urban, Finding F4).</span>`;
        } else {
          bannerEl.innerHTML = `<strong>State Rural-Urban Trajectory (${geo}, ${ind}, 2017–2023):</strong> Insufficient longitudinal observations for this state.<br><span style="font-size:12px; color:#64748b;"><em>All-India Benchmark Reference:</em> Across 36 States/UTs, unweighted female LFPR expansion was rural-led (+24.6 pp rural vs +9.5 pp urban, Finding F4).</span>`;
        }
      }
    }
  }

  function updateAll() {
    updateUCurve();
    updateUR();
    updateRUDivergence();
  }

  geoSel.addEventListener('change', updateAll);
  ucYearSel.addEventListener('change', updateUCurve);
  ucAreaRadios.forEach(r => r.addEventListener('change', updateUCurve));
  urYearSel.addEventListener('change', updateUR);
  ruIndRadios.forEach(r => r.addEventListener('change', updateRUDivergence));

  updateAll();
}

// ------------------------------------------------------------------------------
// TAB 4: Employment & Enterprise Structure
// ------------------------------------------------------------------------------
function initTab4() {
  if (!STATE.tab4) return;
  const data = STATE.tab4;

  const geoSel = document.getElementById('tab4-geography');
  const covSel = document.getElementById('tab4-ind-cov');
  const yrSel = document.getElementById('tab4-year');

  geoSel.innerHTML = data.geographies.map(g => `<option value="${g}">${g}</option>`).join('');
  covSel.innerHTML = Object.entries(data.coverage_labels).map(([k, v]) => `<option value="${k}">${v}</option>`).join('');
  yrSel.innerHTML = data.years.map(y => `<option value="${y}" ${y === 2023 ? 'selected' : ''}>${y}</option>`).join('');

  const areaRadios = document.querySelectorAll('input[name="tab4_area"]');

  function update() {
    const geo = geoSel.value;
    const cov = covSel.value;
    const yr = yrSel.value;
    const area = document.querySelector('input[name="tab4_area"]:checked').value;
    areaRadios.forEach(r => r.parentElement.classList.toggle('active', r.checked));

    const dist = data.distributions_by_geo[geo]?.[cov]?.[yr]?.[area];
    const banner = document.getElementById('tab4-notice-banner');
    const methodBanner = document.getElementById('tab4-methodology-banner');

    if (!dist) return;

    if (dist.is_absent) {
      banner.style.display = 'block';
      banner.className = 'warning-banner';
      banner.innerHTML = `⚠️ <strong>Structural Survey Absence Notice:</strong> ${dist.notice}`;

      if (methodBanner) {
        methodBanner.innerHTML = `<strong>Methodological Notice on Informal Enterprise:</strong> Enterprise classifications follow PLFS Dataset 7131 specifications. Observations are unrecorded for <strong>${geo}</strong> under ${data.coverage_labels[cov]} in ${yr}.<br><span style="font-size:12px; color:#64748b;"><em>All-India Analytical Benchmark:</em> Nationally, proprietary and partnership units account for 56.6% of female non-farm employment. Female workers depend significantly more on public/government sector jobs (24.9% vs 16.0% male) and private household employment (6.3% vs 0.8% male).</span>`;
      }

      // Empty chart with prominent annotation and reduced height
      const layout = {
        title: `Structural Survey Absence: ${geo} (${area}, ${yr})`,
        template: 'plotly_white',
        height: 200,
        margin: { l: 40, r: 40, t: 40, b: 30 },
        annotations: [{
          text: `⚠️ Structural Survey Absence: ${data.coverage_labels[cov]}<br>${dist.notice}<br>Values are strictly unrecorded and never imputed as zero.`,
          xref: 'paper', yref: 'paper',
          x: 0.5, y: 0.5, showarrow: false,
          font: { size: 13, color: '#b91c1c' }
        }],
        xaxis: { showgrid: false, zeroline: false, showticklabels: false },
        yaxis: { showgrid: false, zeroline: false, showticklabels: false }
      };
      Plotly.newPlot('tab4-chart', [], layout, { responsive: true, displayModeBar: false });
    } else {
      banner.style.display = 'none';

      // Update methodology banner dynamically
      if (methodBanner) {
        if (geo === 'All-India (Unweighted Mean)') {
          methodBanner.innerHTML = `<strong>Methodological Notice on Informal Enterprise (All-India Benchmark):</strong> Enterprise classifications follow PLFS Dataset 7131 specifications. Proprietary and partnership units account for 56.6% of female non-farm employment. Female workers depend significantly more on public/government sector jobs (24.9% vs 16.0% male) and private household employment (6.3% vs 0.8% male).`;
        } else {
          const pIdx = dist.enterprise_types.findIndex(t => t.toLowerCase().includes('proprietary'));
          const gIdx = dist.enterprise_types.findIndex(t => t.toLowerCase().includes('govt') || t.toLowerCase().includes('public sector'));
          const hIdx = dist.enterprise_types.findIndex(t => t.toLowerCase().includes('household'));

          const fProp = (pIdx !== -1 && dist.female_shares) ? dist.female_shares[pIdx] : null;
          const mProp = (pIdx !== -1 && dist.male_shares) ? dist.male_shares[pIdx] : null;
          const fGov = (gIdx !== -1 && dist.female_shares) ? dist.female_shares[gIdx] : null;
          const mGov = (gIdx !== -1 && dist.male_shares) ? dist.male_shares[gIdx] : null;
          const fHh = (hIdx !== -1 && dist.female_shares) ? dist.female_shares[hIdx] : null;
          const mHh = (hIdx !== -1 && dist.male_shares) ? dist.male_shares[hIdx] : null;

          const propStr = (fProp !== null && mProp !== null) ? `proprietary and partnership units account for <strong>${fProp.toFixed(1)}%</strong> of female employment (vs ${mProp.toFixed(1)}% male)` : '';
          const govStr = (fGov !== null && mGov !== null) ? `, public/government sector accounts for <strong>${fGov.toFixed(1)}%</strong> (vs ${mGov.toFixed(1)}% male)` : '';
          const hhStr = (fHh !== null && mHh !== null) ? `, and employer's households account for <strong>${fHh.toFixed(1)}%</strong> (vs ${mHh.toFixed(1)}% male)` : '';

          methodBanner.innerHTML = `<strong>Enterprise Distribution Profile (${geo}, ${area}, ${yr}):</strong> In ${geo}, ${propStr}${govStr}${hhStr}.<br><span style="font-size:12px; color:#64748b;"><em>All-India Benchmark Reference:</em> Nationally, proprietary units account for 56.6% of female non-farm employment, public/government enterprises account for 24.9% (vs 16.0% male), and private households account for 6.3% (vs 0.8% male).</span>`;
        }
      }

      const traces = [
        {
          y: dist.enterprise_types,
          x: dist.female_shares,
          orientation: 'h',
          name: 'Female % Engaged',
          type: 'bar',
          marker: { color: '#2563eb' },
          text: dist.female_shares.map(v => v !== null ? `${v.toFixed(1)}%` : 'N/A'),
          textposition: 'outside'
        },
        {
          y: dist.enterprise_types,
          x: dist.male_shares,
          orientation: 'h',
          name: 'Male % Engaged',
          type: 'bar',
          marker: { color: '#94a3b8' },
          text: dist.male_shares.map(v => v !== null ? `${v.toFixed(1)}%` : 'N/A'),
          textposition: 'outside'
        }
      ];

      const xTitle = (geo === 'All-India (Unweighted Mean)')
        ? 'Percentage of Workers Engaged (%) [Unweighted Mean]'
        : `Percentage of Workers Engaged (%) [${geo}]`;

      const layout = {
        title: `Enterprise Distribution: ${data.coverage_labels[cov]} (${geo}, ${area}, ${yr})`,
        xaxis: { title: xTitle, range: [0, 90] },
        yaxis: { title: 'Enterprise Type', automargin: true },
        barmode: 'group',
        template: 'plotly_white',
        legend: { orientation: 'h', yanchor: 'bottom', y: 1.02, xanchor: 'right', x: 1 },
        margin: { l: 200, r: 40, t: 60, b: 40 },
        height: 440
      };
      Plotly.newPlot('tab4-chart', traces, layout, { responsive: true, displayModeBar: false });
    }
  }

  geoSel.addEventListener('change', update);
  covSel.addEventListener('change', update);
  yrSel.addEventListener('change', update);
  areaRadios.forEach(r => r.addEventListener('change', update));

  update();
}

// ------------------------------------------------------------------------------
// TAB 5: Empirical Evidence & Methodology
// ------------------------------------------------------------------------------
function initTab5() {
  if (!STATE.tab5) return;
  const data = STATE.tab5;

  // Populate Phase 6 Table
  const p6Tbody = document.querySelector('#tab5-phase6-table tbody');
  p6Tbody.innerHTML = data.phase6_tests.map(r => `
    <tr>
      <td><strong>${r.Finding}</strong></td>
      <td>${r.Analysis}</td>
      <td>${r.Test}</td>
      <td>${r.Statistic !== null ? r.Statistic.toFixed(2) : 'N/A'}</td>
      <td><strong>${r.p_value}</strong></td>
      <td>${r.Effect_Size !== null ? r.Effect_Size.toFixed(3) : 'N/A'}</td>
    </tr>
  `).join('');

  // Populate Phase 7 ML Table
  const mlTbody = document.querySelector('#tab5-ml-table tbody');
  mlTbody.innerHTML = data.phase7_ml_models.map(r => `
    <tr>
      <td><strong>${r.Model}</strong></td>
      <td>${r.Validation_Method}</td>
      <td>${r.Total_Folds}</td>
      <td>${r.MAE.toFixed(3)}</td>
      <td>${r.RMSE.toFixed(3)}</td>
      <td>${r.R2.toFixed(3)}</td>
    </tr>
  `).join('');

  // Populate Importance Table
  const impTbody = document.querySelector('#tab5-imp-table tbody');
  impTbody.innerHTML = data.phase7_feature_importance.map(r => `
    <tr>
      <td>${r.Feature}</td>
      <td>${r.Ridge_Coefficient !== null ? r.Ridge_Coefficient.toFixed(2) : '—'}</td>
      <td>${r.GBR_Feature_Importance !== null ? r.GBR_Feature_Importance.toFixed(4) : '—'}</td>
    </tr>
  `).join('');
}

// ------------------------------------------------------------------------------
// TAB 6: Forecasting Outlook (1-Year Horizon)
// ------------------------------------------------------------------------------
function initTab6() {
  if (!STATE.tab6) return;
  const data = STATE.tab6;

  const ALL_INDIA_LABEL = 'All-India Analytical Mean (Unweighted across 36 States/UTs)';
  const ALL_INDIA_KEY = 'National (All States)';

  // Populate Selectors
  const stSel = document.getElementById('tab6-state');
  const stateOptions = [ALL_INDIA_LABEL, ...data.states.filter(s => s !== ALL_INDIA_KEY)];
  stSel.innerHTML = stateOptions.map(s => `<option value="${s}">${s}</option>`).join('');

  const indRadios = document.querySelectorAll('input[name="tab6_ind"]');
  const genRadios = document.querySelectorAll('input[name="tab6_gen"]');
  const areaRadios = document.querySelectorAll('input[name="tab6_area"]');

  function update() {
    const rawState = stSel.value;
    const internalState = rawState === ALL_INDIA_LABEL ? ALL_INDIA_KEY : rawState;
    const ind = document.querySelector('input[name="tab6_ind"]:checked').value;
    const gen = document.querySelector('input[name="tab6_gen"]:checked').value;
    const area = document.querySelector('input[name="tab6_area"]:checked').value;

    indRadios.forEach(r => r.parentElement.classList.toggle('active', r.checked));
    genRadios.forEach(r => r.parentElement.classList.toggle('active', r.checked));
    areaRadios.forEach(r => r.parentElement.classList.toggle('active', r.checked));

    // Resolve Scenario (Default to Education: 'All')
    const key = `${internalState}|${ind}|${gen}|${area}|All`;
    const scenario = data.scenarios[key] || null;

    renderTab6Kpis(scenario);
    renderTab6Chart(rawState, ind, gen, area, scenario);
    renderTab6Explanatory(scenario);
  }

  stSel.addEventListener('change', update);
  indRadios.forEach(r => r.addEventListener('change', update));
  genRadios.forEach(r => r.addEventListener('change', update));
  areaRadios.forEach(r => r.addEventListener('change', update));

  update();
}

function renderTab6Kpis(scenario) {
  if (!scenario) {
    document.getElementById('tab6-kpi-ribbon').innerHTML = renderKpiCard('Scenario Status', 'Data Unavailable', 'No matching scenario found in results', 'Error');
    return;
  }

  const status = scenario.Eligibility_Status;
  const baseYr = scenario.Historical_End_Year;
  const fcYr = scenario.Forecast_Year;
  const fcVal = scenario.Forecast_Value;
  const modelName = scenario.Selected_Model;
  const modelMae = scenario.Model_MAE;
  const naiveMae = scenario.Naive_Baseline_MAE;
  const lowerInt = scenario.Lower_Interval_80;
  const upperInt = scenario.Upper_Interval_80;

  const validInt = lowerInt !== null && upperInt !== null && isFinite(lowerInt) && isFinite(upperInt) && lowerInt <= upperInt;

  let badgeStyle = '';
  let badgeText = '';
  let valStr = 'Suppressed';
  let subStr = scenario.Eligibility_Reason;
  let intStr = 'N/A (Projection Suppressed)';

  if (status === 'FORECAST_ELIGIBLE') {
    badgeStyle = 'background:#dcfce7; color:#15803d;';
    badgeText = 'FORECAST ELIGIBLE — VALIDATED';
    valStr = fcVal !== null ? `${fcVal.toFixed(2)}%` : 'N/A';
    subStr = `Model: ${modelName} (MAE: ${modelMae.toFixed(2)} pp vs. Naive: ${naiveMae.toFixed(2)} pp)`;
    intStr = validInt ? `[${lowerInt.toFixed(2)}%, ${upperInt.toFixed(2)}%]` : 'Unavailable / Invalid';
  } else if (status === 'FORECAST_ELIGIBLE_WITH_LIMITATIONS') {
    badgeStyle = 'background:#fef3c7; color:#b45309;';
    badgeText = 'ELIGIBLE WITH LIMITATIONS';
    valStr = fcVal !== null ? `${fcVal.toFixed(2)}%` : 'N/A';
    subStr = `Caution: ${modelName} (MAE: ${modelMae.toFixed(2)} pp)`;
    intStr = validInt ? `[${lowerInt.toFixed(2)}%, ${upperInt.toFixed(2)}%]` : 'Unavailable / Invalid';
  } else {
    badgeStyle = 'background:#fee2e2; color:#b91c1c;';
    badgeText = 'FORECAST NOT SUPPORTED';
    valStr = 'Suppressed';
    subStr = 'Exceeded error threshold or discontinuous series';
    intStr = 'N/A (Projection Suppressed)';
  }

  const c1 = `
    <div class="kpi-card">
      <div class="kpi-header">
        <span class="kpi-title">Eligibility Status</span>
        <span class="kpi-badge" style="${badgeStyle}">${badgeText}</span>
      </div>
      <div class="kpi-value" style="font-size: 20px;">${status.replace(/_/g, ' ')}</div>
      <div class="kpi-subtext">Base Year: ${baseYr} → Outlook Year: ${fcYr}</div>
    </div>
  `;
  const c2 = renderKpiCard(`${fcYr} Point Forecast`, valStr, subStr, 'Horizon: 1-Year');
  const c3 = renderKpiCard('Empirical Uncertainty Interval', intStr, '80% Nominal Bound (from validation residuals)', 'Uncertainty');

  document.getElementById('tab6-kpi-ribbon').innerHTML = `${c1}${c2}${c3}`;
}

function renderTab6Chart(stateDisplay, indicator, gender, areaType, scenario) {
  if (!scenario || !scenario.Historical_Years || scenario.Historical_Years.length === 0) {
    const layout = {
      title: `Historical Trajectory: ${indicator} (${stateDisplay}) - No Data Available`,
      template: 'plotly_white',
      height: 420,
      annotations: [{
        text: '⚠️ No historical observations available for this series.',
        showarrow: false,
        font: { size: 13, color: '#b91c1c' },
        bgcolor: '#fee2e2', bordercolor: '#fca5a5', borderwidth: 1, borderpad: 8
      }],
      xaxis: { showgrid: false, zeroline: false, showticklabels: false },
      yaxis: { showgrid: false, zeroline: false, showticklabels: false }
    };
    Plotly.newPlot('tab6-chart', [], layout, { responsive: true, displayModeBar: false });
    return;
  }

  const histYears = scenario.Historical_Years;
  const histVals = scenario.Historical_Values;
  const baseYear = Math.max(...histYears);
  const boundaryX = baseYear + 0.5;

  const traces = [
    {
      x: histYears,
      y: histVals,
      mode: 'lines+markers+text',
      name: 'Observed Historical Data',
      line: { color: '#2563eb', width: 3 },
      marker: { size: 8, color: '#2563eb' },
      text: histVals.map(v => v !== null ? `${v.toFixed(1)}%` : 'N/A'),
      textposition: 'top center',
      textfont: { size: 11, color: '#1e3a8a' }
    }
  ];

  const isEligible = scenario.Eligibility_Status === 'FORECAST_ELIGIBLE' || scenario.Eligibility_Status === 'FORECAST_ELIGIBLE_WITH_LIMITATIONS';
  const lowerInt = scenario.Lower_Interval_80;
  const upperInt = scenario.Upper_Interval_80;
  const validInt = lowerInt !== null && upperInt !== null && isFinite(lowerInt) && isFinite(upperInt) && lowerInt <= upperInt;

  const shapes = [
    {
      type: 'line',
      x0: boundaryX, x1: boundaryX,
      y0: 0, y1: 1, yref: 'paper',
      line: { color: '#94a3b8', width: 1.5, dash: 'dot' }
    }
  ];

  const annotations = [
    {
      x: boundaryX, y: 1, yref: 'paper',
      text: 'Forecast Horizon Start',
      showarrow: false,
      xanchor: 'right', yanchor: 'top',
      font: { size: 10, color: '#64748b' }
    }
  ];

  if (isEligible) {
    const fcYr = scenario.Forecast_Year;
    const fcVal = scenario.Forecast_Value;
    const lastHistVal = histVals[histVals.length - 1];

    // Projection dashed path
    traces.push({
      x: [baseYear, fcYr],
      y: [lastHistVal, fcVal],
      mode: 'lines',
      name: '1-Year Projection Path',
      line: { color: '#d97706', width: 2.5, dash: 'dash' },
      showlegend: false
    });

    // Uncertainty Interval Bar
    if (validInt) {
      traces.push({
        x: [fcYr, fcYr],
        y: [lowerInt, upperInt],
        mode: 'lines+markers',
        name: 'Empirical Uncertainty Interval (80% Nominal)',
        line: { color: '#f59e0b', width: 6 },
        marker: { symbol: 'line-ew', size: 14, color: '#b45309' },
        hoverinfo: 'text',
        hovertext: `80% Nominal Interval: [${lowerInt.toFixed(2)}%, ${upperInt.toFixed(2)}%]`
      });
    }

    // Forecast Point Marker
    traces.push({
      x: [fcYr],
      y: [fcVal],
      mode: 'markers+text',
      name: `Forecast Point (${scenario.Selected_Model})`,
      marker: { size: 12, symbol: 'diamond', color: '#d97706', line: { color: '#78350f', width: 1.5 } },
      text: [`${fcVal.toFixed(2)}% [Proj]`],
      textposition: 'top center',
      textfont: { size: 11, color: '#78350f' }
    });

    // Background Shading Rect
    shapes.push({
      type: 'rect',
      x0: boundaryX, x1: fcYr + 0.5,
      y0: 0, y1: 1, yref: 'paper',
      fillcolor: 'rgba(245, 158, 11, 0.08)',
      line: { width: 0 },
      layer: 'below'
    });
    annotations.push({
      x: fcYr + 0.5, y: 0, yref: 'paper',
      text: `Model Outlook (${fcYr})`,
      showarrow: false,
      xanchor: 'right', yanchor: 'bottom',
      font: { size: 11, color: '#b45309' }
    });
  } else {
    // Unsupported Annotation
    annotations.push({
      x: baseYear + 0.8,
      y: histVals.reduce((a, b) => a + (b || 0), 0) / histVals.length,
      text: `⚠️ Projection Suppressed:<br>${scenario.Eligibility_Reason}`,
      showarrow: false,
      font: { size: 11, color: '#b91c1c' },
      bgcolor: '#fee2e2', bordercolor: '#fca5a5', borderwidth: 1, borderpad: 6
    });
  }

  // Y-axis scaling (Strictly historical for unsupported)
  const allY = [...histVals.filter(v => v !== null)];
  if (isEligible) {
    if (scenario.Forecast_Value !== null) allY.push(scenario.Forecast_Value);
    if (validInt) allY.push(lowerInt, upperInt);
  }

  const yMin = Math.max(0.0, Math.min(...allY) - 5.0);
  const yMax = Math.min(100.0, Math.max(...allY) + 8.0);

  const layout = {
    title: `Historical Trajectory and 1-Year Forecasting Outlook: ${indicator} (${stateDisplay})`,
    xaxis: { title: 'Survey Wave / Projection Year', dtick: 1 },
    yaxis: { title: `${indicator} (%)`, range: [yMin, yMax] },
    shapes: shapes,
    annotations: annotations,
    template: 'plotly_white',
    legend: { orientation: 'h', yanchor: 'bottom', y: 1.02, xanchor: 'right', x: 1 },
    margin: { l: 50, r: 40, t: 60, b: 40 },
    height: 420
  };

  Plotly.newPlot('tab6-chart', traces, layout, { responsive: true, displayModeBar: false });
}

function renderTab6Explanatory(scenario) {
  if (!scenario) return;

  const status = scenario.Eligibility_Status;
  const reason = scenario.Eligibility_Reason;
  const modelName = scenario.Selected_Model;
  const modelMae = scenario.Model_MAE;
  const naiveMae = scenario.Naive_Baseline_MAE;
  const improvement = scenario.MAE_Improvement_vs_Baseline;

  let statusBox = '';
  if (status === 'FORECAST_ELIGIBLE') {
    statusBox = `
      <div style="background:#f0fdf4; border-left:4px solid #16a34a; padding:12px 16px; border-radius:4px; margin-bottom:14px; color:#166534;">
        <strong>🟢 Validated Forecast:</strong> This scenario meets strict out-of-sample accuracy standards (MAE ≤ 4.0 pp) and demonstrates verifiable improvement over the Naive baseline. The <strong>${modelName}</strong> model was deterministically selected across expanding historical validation origins.
      </div>
    `;
  } else if (status === 'FORECAST_ELIGIBLE_WITH_LIMITATIONS') {
    statusBox = `
      <div style="background:#fffbeb; border-left:4px solid #d97706; padding:12px 16px; border-radius:4px; margin-bottom:14px; color:#92400e;">
        <strong>🟡 Caution — Eligible with Limitations:</strong> ${reason}<br>
        Model: <strong>${modelName}</strong> achieved an out-of-sample MAE of ${modelMae.toFixed(2)} pp. Users should treat this outlook with caution, recognizing higher cyclical or baseline volatility.
      </div>
    `;
  } else {
    statusBox = `
      <div style="background:#fef2f2; border-left:4px solid #dc2626; padding:12px 16px; border-radius:4px; margin-bottom:14px; color:#991b1b;">
        <strong>🔴 Forecast Not Supported:</strong> ${reason}<br>
        In accordance with empirical safeguards, projections for this scenario are <strong>suppressed</strong> because error thresholds were exceeded or the historical series lacks continuous observations. No arbitrary or zero values are plotted.
      </div>
    `;
  }

  const validationDetail = status !== 'FORECAST_NOT_SUPPORTED' ? `
    <h4 style="margin-bottom:8px; color:#1e293b;">Model Selection & Backtesting Metrics:</h4>
    <ul>
      <li>Selected Model: <code>${modelName}</code></li>
      <li>Out-of-Sample MAE across 3 Rolling Origins: <code>${modelMae.toFixed(2)} pp</code></li>
      <li>Naive Baseline MAE: <code>${naiveMae.toFixed(2)} pp</code></li>
      <li>Net Improvement over Baseline: <code>${improvement >= 0 ? '+' : ''}${improvement.toFixed(2)} pp</code></li>
    </ul>
  ` : `
    <h4 style="margin-bottom:8px; color:#1e293b;">Methodological Rejection Rationale:</h4>
    <ul>
      <li>Reason: ${reason}</li>
      <li>Candidate Model MAE: <code>${modelMae !== null ? modelMae.toFixed(2) : 'N/A'} pp</code> vs. Naive Baseline: <code>${naiveMae !== null ? naiveMae.toFixed(2) : 'N/A'} pp</code></li>
    </ul>
  `;

  document.getElementById('tab6-explanatory-box').innerHTML = `${statusBox}${validationDetail}`;
}

// ------------------------------------------------------------------------------
// GLOBAL INITIALIZATION & TAB SWITCHING
// ------------------------------------------------------------------------------
async function loadData() {
  const loadingEl = document.getElementById('global-loading');
  const errorEl = document.getElementById('global-error');

  try {
    const [t1, t2, t3, t4, t5, t6] = await Promise.all([
      fetch('data/tab1_national.json').then(r => r.json()),
      fetch('data/tab2_states.json').then(r => r.json()),
      fetch('data/tab3_fault_lines.json').then(r => r.json()),
      fetch('data/tab4_enterprise.json').then(r => r.json()),
      fetch('data/tab5_evidence.json').then(r => r.json()),
      fetch('data/tab6_forecasts.json').then(r => r.json())
    ]);

    STATE.tab1 = t1;
    STATE.tab2 = t2;
    STATE.tab3 = t3;
    STATE.tab4 = t4;
    STATE.tab5 = t5;
    STATE.tab6 = t6;

    loadingEl.style.display = 'none';

    // Init All Tabs
    initTab1();
    initTab2();
    initTab3();
    initTab4();
    initTab5();
    initTab6();
  } catch (err) {
    loadingEl.style.display = 'none';
    errorEl.style.display = 'block';
    errorEl.innerHTML = `<strong>Failed to load analytical data files:</strong> ${err.message}. Please verify JSON paths.`;
    console.error('Data loading error:', err);
  }
}

function setupTabNavigation() {
  const navBtns = document.querySelectorAll('.tab-btn');
  const panes = document.querySelectorAll('.tab-pane');

  navBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetId = btn.getAttribute('data-tab');
      navBtns.forEach(b => b.classList.toggle('active', b === btn));
      panes.forEach(p => p.classList.toggle('active', p.id === targetId));

      // Trigger Plotly relayout to fit newly visible tab containers
      window.dispatchEvent(new Event('resize'));
    });
  });
}

document.addEventListener('DOMContentLoaded', () => {
  setupTabNavigation();
  loadData();
});
