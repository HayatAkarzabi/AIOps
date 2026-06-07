// ===== Navigation: switch between sections =====
function switchSection(sectionId) {
    // Update sidebar active state
    document.querySelectorAll('.nav-links li').forEach(function (li) {
        li.classList.toggle('active', li.dataset.section === sectionId);
    });

    // Show the corresponding content section
    document.querySelectorAll('.content-section').forEach(function (section) {
        section.classList.toggle('active', section.id === 'section-' + sectionId);
    });

    // Update the topbar title
    var titles = {
        dashboard: 'Dashboard',
        metrics: 'Metrics',
        logs: 'Logs',
        anomalies: 'Anomalies',
        forecasts: 'Forecasts',
        alerts: 'Alerts'
    };
    document.getElementById('section-title').textContent = titles[sectionId] || 'Dashboard';
}

// Attach click handlers to sidebar items
document.querySelectorAll('.nav-links li').forEach(function (li) {
    li.addEventListener('click', function () {
        switchSection(li.dataset.section);
    });
});

// ===== API Base URL =====
var API_BASE = 'http://localhost:8000';

// ===== Helper: fetch JSON from an endpoint =====
function apiFetch(endpoint) {
    return fetch(API_BASE + endpoint)
        .then(function (response) {
            if (!response.ok) {
                throw new Error('HTTP ' + response.status);
            }
            return response.json();
        });
}

// ===== Load Health Status =====
function loadHealth() {
    apiFetch('/health').then(function (data) {
        var el = document.getElementById('health-status');
        el.textContent = data.status || 'Unknown';
        el.className = 'health-indicator ' + (data.status === 'healthy' ? 'healthy' : 'degraded');
        document.getElementById('health-message').textContent =
            'Service: ' + (data.service || 'AIOps Platform') +
            ' — Version: ' + (data.version || '1.0.0');
    }).catch(function () {
        document.getElementById('health-status').textContent = 'Offline';
        document.getElementById('health-status').className = 'health-indicator error';
        document.getElementById('health-message').textContent = 'Cannot reach the API server. Make sure it is running on ' + API_BASE;
    });
}

// ===== Load Metrics =====
function loadMetrics() {
    apiFetch('/metrics').then(function (data) {
        var el = document.getElementById('metrics-content');
        if (!data || data.length === 0) {
            el.innerHTML = '<p style="color:#8b949e;">No metrics data available.</p>';
            return;
        }
        document.getElementById('stat-metrics').textContent = data.length;
        var table = '<table><thead><tr><th>Name</th><th>Value</th><th>Unit</th><th>Timestamp</th></tr></thead><tbody>';
        data.forEach(function (m) {
            table += '<tr><td>' + m.name + '</td><td>' + m.value + '</td><td>' + (m.unit || '') + '</td><td>' + (m.timestamp || '') + '</td></tr>';
        });
        table += '</tbody></table>';
        el.innerHTML = table;
    }).catch(function () {
        document.getElementById('metrics-content').innerHTML = '<p style="color:#f85149;">Failed to load metrics.</p>';
    });
}

// ===== Load Logs =====
function loadLogs() {
    apiFetch('/logs').then(function (data) {
        var el = document.getElementById('logs-content');
        if (!data || data.length === 0) {
            el.innerHTML = '<p style="color:#8b949e;">No logs available.</p>';
            return;
        }
        document.getElementById('stat-logs').textContent = data.length;
        var html = '<div class="data-stream">';
        data.forEach(function (log) {
            var levelClass = 'level-' + (log.level || 'info').toLowerCase();
            html += '<div class="stream-item">' +
                '<span class="timestamp">' + (log.timestamp || '') + '</span>' +
                '<span class="level ' + levelClass + '">' + (log.level || 'INFO') + '</span>' +
                '<span class="message">' + (log.message || log.source || '') + '</span>' +
                '</div>';
        });
        html += '</div>';
        el.innerHTML = html;
    }).catch(function () {
        document.getElementById('logs-content').innerHTML = '<p style="color:#f85149;">Failed to load logs.</p>';
    });
}

// ===== Load Anomalies =====
function loadAnomalies() {
    apiFetch('/anomalies').then(function (data) {
        var el = document.getElementById('anomalies-content');
        if (!data || data.length === 0) {
            el.innerHTML = '<p style="color:#8b949e;">No anomalies detected.</p>';
            return;
        }
        document.getElementById('stat-anomalies').textContent = data.length;
        var table = '<table><thead><tr><th>Metric</th><th>Score</th><th>Severity</th><th>Timestamp</th></tr></thead><tbody>';
        data.forEach(function (a) {
            var sevClass = 'severity-' + (a.severity || 'low').toLowerCase();
            table += '<tr><td>' + (a.metric_name || '') + '</td><td>' + (a.anomaly_score || a.score || '') + '</td>' +
                '<td class="' + sevClass + '">' + (a.severity || '') + '</td><td>' + (a.timestamp || '') + '</td></tr>';
        });
        table += '</tbody></table>';
        el.innerHTML = table;
    }).catch(function () {
        document.getElementById('anomalies-content').innerHTML = '<p style="color:#f85149;">Failed to load anomalies.</p>';
    });
}

// ===== Load Forecasts =====
function loadForecasts() {
    apiFetch('/forecasts').then(function (data) {
        var el = document.getElementById('forecasts-content');
        if (!data || data.length === 0) {
            el.innerHTML = '<p style="color:#8b949e;">No forecast data available.</p>';
            return;
        }
        var table = '<table><thead><tr><th>Metric</th><th>Forecasted Value</th><th>Lower Bound</th><th>Upper Bound</th><th>Timestamp</th></tr></thead><tbody>';
        data.forEach(function (f) {
            table += '<tr><td>' + (f.metric_name || '') + '</td><td>' + (f.forecasted_value || '') + '</td>' +
                '<td>' + (f.lower_bound || '') + '</td><td>' + (f.upper_bound || '') + '</td><td>' + (f.timestamp || '') + '</td></tr>';
        });
        table += '</tbody></table>';
        el.innerHTML = table;
    }).catch(function () {
        document.getElementById('forecasts-content').innerHTML = '<p style="color:#f85149;">Failed to load forecasts.</p>';
    });
}

// ===== Load Alerts =====
function loadAlerts() {
    apiFetch('/alerts').then(function (data) {
        var el = document.getElementById('alerts-content');
        if (!data || data.length === 0) {
            el.innerHTML = '<p style="color:#8b949e;">No active alerts.</p>';
            return;
        }
        document.getElementById('stat-alerts').textContent = data.length;
        var table = '<table><thead><tr><th>Rule</th><th>Severity</th><th>Status</th><th>Message</th><th>Timestamp</th></tr></thead><tbody>';
        data.forEach(function (a) {
            var sevClass = 'severity-' + (a.severity || 'low').toLowerCase();
            var statusClass = 'status-' + (a.status || 'active').toLowerCase();
            table += '<tr><td>' + (a.rule_name || '') + '</td>' +
                '<td class="' + sevClass + '">' + (a.severity || '') + '</td>' +
                '<td class="' + statusClass + '">' + (a.status || '') + '</td>' +
                '<td>' + (a.message || '') + '</td>' +
                '<td>' + (a.timestamp || '') + '</td></tr>';
        });
        table += '</tbody></table>';
        el.innerHTML = table;
    }).catch(function () {
        document.getElementById('alerts-content').innerHTML = '<p style="color:#f85149;">Failed to load alerts.</p>';
    });
}

// ===== Refresh All Data =====
function refreshAll() {
    loadHealth();
    loadMetrics();
    loadLogs();
    loadAnomalies();
    loadForecasts();
    loadAlerts();
}

// ===== Auto-refresh every 30 seconds =====
setInterval(refreshAll, 30000);

// ===== Initial load on page ready =====
document.addEventListener('DOMContentLoaded', refreshAll);
