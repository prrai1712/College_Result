let allResults = [];

async function fetchAllResults() {
    const scholarno = document.getElementById("scholarno").value;
    const resultDiv = document.getElementById("result");
    const semesterSelectWrapper = document.getElementById("semesterSelectWrapper");
    const semesterSelect = document.getElementById("semester");

    if (!scholarno) {
        resultDiv.innerHTML = "<p>Please enter a Scholar Number.</p>";
        return;
    }

    resultDiv.innerHTML = "<p>Fetching results...</p>";

    try {
        const response = await fetch("https://college-result-1phb.onrender.com/fetch-student-result", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ scholarno: scholarno, semester: 1 })
        });

        if (!response.ok) throw new Error("Failed to fetch result.");

        const data = await response.json();
        if (!Array.isArray(data)) {
            resultDiv.innerHTML = "<p>Invalid response from server.</p>";
            return;
        }

        allResults = data;
        semesterSelect.innerHTML = "";

        data.forEach((res, idx) => {
            const opt = document.createElement("option");
            opt.value = idx;
            opt.text = `Semester ${res.Semester}`;
            semesterSelect.appendChild(opt);
        });

        semesterSelectWrapper.style.display = "block";
        displaySemesterResult();

    } catch (err) {
        resultDiv.innerHTML = `<p style="color:red;">Error: ${err.message}</p>`;
    }
}

function displaySemesterResult() {
    const resultDiv = document.getElementById("result");
    const selectedIndex = document.getElementById("semester").value;
    const res = allResults[selectedIndex];

    if (!res) return;

    resultDiv.innerHTML = `
        <div><strong>Name:</strong> ${res.StudentName}</div>
        <div><strong>Scholar No:</strong> ${res.ScholarNo}</div>
        <div><strong>Semester:</strong> ${res.Semester}</div>
        <div><strong>Result:</strong> ${res.Result}</div>
        <div><strong>Obtained:</strong> ${res.ObtainGrandTotal}</div>
        <div><strong>Total:</strong> ${res.MaxGrandTotal}</div>
        <div><strong>SGPA:</strong> ${res.SGPA}</div>
        <div><strong>CGPA:</strong> ${res.CGPA}</div>
        <div><strong>Percentage:</strong> ${res.Percentage}</div>
    `;
}

/* ---------- Theme Toggle ---------- */
const themeToggle = document.getElementById("theme-toggle");
const themeIcon = document.getElementById("theme-icon");

function setTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
    themeIcon.textContent = theme === "dark" ? "☀️" : "🌙";
}

function toggleTheme() {
    const current = localStorage.getItem("theme") || "system";
    const next = current === "dark" ? "light" : "dark";
    setTheme(next);
}

themeToggle.addEventListener("click", toggleTheme);

(function initTheme() {
    const saved = localStorage.getItem("theme") || "system";
    if (saved === "system") {
        const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
        setTheme(prefersDark ? "dark" : "light");
    } else {
        setTheme(saved);
    }
})();
