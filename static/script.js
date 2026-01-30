function uploadAPK() {
    const fileInput = document.getElementById("apkFile");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select an APK file");
        return;
    }

    const formData = new FormData();
    formData.append("apk", file);

    fetch("/analyze", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            document.getElementById("output").innerHTML =
                `<p class="error">${data.error}</p>`;
            return;
        }

        let html = `
            <h3>App Name: ${data.app_name}</h3>
            <p>Package: ${data.package_name}</p>
            <p>Total Permissions: ${data.total_permissions}</p>
            <table>
                <tr><th>Permission</th><th>Risk</th></tr>
        `;

        data.permissions.forEach(p => {
            html += `<tr>
                        <td>${p.permission}</td>
                        <td class="${p.risk.toLowerCase()}">${p.risk}</td>
                     </tr>`;
        });

        html += "</table>";
        document.getElementById("output").innerHTML = html;
    })
    .catch(() => {
        document.getElementById("output").innerHTML =
            "<p class='error'>Analysis failed</p>";
    });
}
