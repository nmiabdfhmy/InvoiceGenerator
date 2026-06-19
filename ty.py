import os
from weasyprint import HTML

html_content = """<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Master Service of Agreement & Invoice</title>
    <style>
        /* General Reset & Setup */
        *, *::before, *::after {
            box-sizing: border-box;
        }
        body {
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Helvetica, Arial, sans-serif;
            color: #1e293b;
            line-height: 1.6;
            font-size: 10pt;
            background-color: #fafbfc;
        }

        /* Page Rules with Custom Elegant Borders/Overlays */
        @page {
            size: A4;
            margin: 25mm 20mm 25mm 20mm;
            background-color: #fafbfc;
            
            /* Page Overlay: Tech-style thin frames around margins */
            border-top: 4px solid #0f172a;
            border-bottom: 4px solid #0284c7;
            
            @bottom-right {
                content: "Halaman " counter(page) " dari " counter(pages);
                font-size: 8pt;
                color: #64748b;
                font-weight: 600;
                font-family: 'Segoe UI', sans-serif;
            }
            @bottom-left {
                content: "MASTER SERVICE OF AGREEMENT • INV-TOS/2026/001";
                font-size: 8pt;
                color: #0284c7;
                font-weight: 700;
                letter-spacing: 0.5px;
                font-family: 'Segoe UI', sans-serif;
            }
        }

        /* Cover Page Layout */
        .cover-page {
            page-break-after: always;
            height: 100%;
            margin-top: -5mm;
            position: relative;
        }
        
        /* High-fidelity Tech Decorative Cover Overlay */
        .cover-accent-line {
            width: 80px;
            height: 4px;
            background: #0284c7;
            margin-bottom: 8mm;
        }
        
        .cover-hero {
            background-color: #0f172a;
            color: #ffffff;
            /* Extending into the page margins for full-bleed look */
            margin: -25mm -20mm 15mm -20mm;
            padding: 45mm 20mm 30mm 20mm;
            border-bottom: 6px solid #0284c7;
            position: relative;
        }
        
        /* Geometric watermark overlay effect using CSS */
        .cover-hero::after {
            content: "";
            position: absolute;
            top: 0; right: 0; bottom: 0; left: 0;
            background: linear-gradient(135deg, rgba(2, 132, 199, 0.15) 0%, transparent 70%);
            pointer-events: none;
        }

        .cover-title {
            font-size: 28pt;
            font-weight: 800;
            line-height: 1.15;
            margin: 0 0 4mm 0;
            letter-spacing: -0.5px;
            text-transform: uppercase;
            color: #ffffff;
        }
        .cover-subtitle {
            font-size: 12pt;
            font-weight: 600;
            color: #38bdf8;
            margin: 0;
            letter-spacing: 1px;
            text-transform: uppercase;
        }
        
        .cover-meta-container {
            margin-top: 20mm;
            display: table;
            width: 100%;
        }
        .cover-meta-row {
            display: table-row;
        }
        .cover-meta-cell {
            display: table-cell;
            width: 50%;
            padding-bottom: 6mm;
            vertical-align: top;
        }
        .meta-label {
            font-size: 8.5pt;
            text-transform: uppercase;
            color: #64748b;
            letter-spacing: 1px;
            margin-bottom: 1.5mm;
            font-weight: 700;
        }
        .meta-value {
            font-size: 11pt;
            font-weight: 600;
            color: #1e293b;
        }

        /* Section Typography */
        h1 {
            font-size: 16pt;
            color: #0f172a;
            margin-top: 0;
            margin-bottom: 10mm;
            font-weight: 800;
            border-bottom: 2px solid #0f172a;
            padding-bottom: 2mm;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            page-break-after: avoid;
        }
        h2 {
            font-size: 12pt;
            color: #0f172a;
            margin-top: 8mm;
            margin-bottom: 4mm;
            font-weight: 700;
            border-left: 4px solid #0284c7;
            padding-left: 3mm;
            text-transform: uppercase;
            letter-spacing: 0.3px;
            page-break-after: avoid;
        }

        /* Global Elements */
        p {
            margin-top: 0;
            margin-bottom: 4mm;
            text-align: justify;
            color: #334155;
        }
        ol, ul {
            margin-top: 0;
            margin-bottom: 5mm;
            padding-left: 5mm;
            color: #334155;
        }
        li {
            margin-bottom: 2mm;
            text-align: justify;
        }

        /* Tables */
        .invoice-section {
            page-break-after: always;
        }
        .invoice-top-table {
            display: table;
            width: 100%;
            margin-bottom: 8mm;
        }
        .invoice-top-row {
            display: table-row;
        }
        .invoice-top-cell {
            display: table-cell;
            vertical-align: top;
        }
        
        table.premium-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 4mm;
            margin-bottom: 6mm;
        }
        table.premium-table th {
            background-color: #0f172a;
            color: #ffffff;
            font-weight: 700;
            text-align: left;
            padding: 3.5mm 4mm;
            font-size: 9.5pt;
            border: 1px solid #0f172a;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        table.premium-table td {
            padding: 3.5mm 4mm;
            border: 1px solid #e2e8f0;
            font-size: 9.5pt;
            vertical-align: top;
            background-color: #ffffff;
        }
        table.premium-table tr:nth-child(even) td {
            background-color: #f8fafc;
        }
        
        .text-right { text-align: right !important; }
        .text-center { text-align: center !important; }
        .font-bold { font-weight: bold; }

        /* Summary Splitting */
        .summary-wrapper {
            display: table;
            width: 100%;
            margin-top: 4mm;
        }
        .summary-row { display: table-row; }
        .summary-left { display: table-cell; width: 40%; }
        .summary-right { display: table-cell; width: 60%; }
        
        table.summary-block {
            width: 100%;
            border-collapse: collapse;
        }
        table.summary-block td {
            padding: 2.5mm 4mm;
            border-bottom: 1px solid #e2e8f0;
            font-size: 9.5pt;
        }
        table.summary-block tr.grand-total td {
            border-top: 2px solid #0f172a;
            border-bottom: 2px solid #0f172a;
            font-weight: 700;
            background-color: #f1f5f9;
            color: #0f172a;
        }

        /* Modern Package Grid Simulator via Table */
        .package-table {
            width: 100%;
            margin-bottom: 6mm;
            border-collapse: collapse;
            page-break-inside: avoid;
        }
        .package-card {
            border: 1px solid #e2e8f0;
            background: #ffffff;
            padding: 5mm;
            margin-bottom: 4mm;
            border-radius: 4px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02);
            page-break-inside: avoid;
        }
        .package-badge {
            display: inline-block;
            font-size: 8pt;
            font-weight: 700;
            background-color: #e0f2fe;
            color: #0369a1;
            padding: 1mm 2.5mm;
            border-radius: 9999px;
            text-transform: uppercase;
            margin-bottom: 2mm;
        }
        .package-name {
            font-size: 11pt;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 2mm;
        }

        /* Warning Banner / Callout Box */
        .legal-warning-box {
            background-color: #fef2f2;
            border-left: 4px solid #ef4444;
            padding: 4mm 5mm;
            margin: 6mm 0;
            page-break-inside: avoid;
        }
        .legal-warning-box h3 {
            color: #991b1b;
            margin-top: 0;
            margin-bottom: 1.5mm;
            text-transform: uppercase;
            font-size: 10.5pt;
            font-weight: 700;
            letter-spacing: 0.5px;
        }
        .legal-warning-box p {
            color: #7f1d1d;
            margin-bottom: 0;
            font-size: 9.5pt;
        }

        /* Signatures Container */
        .signatures-container {
            margin-top: 12mm;
            page-break-inside: avoid;
        }
        .sigs-table {
            display: table;
            width: 100%;
            margin-top: 8mm;
        }
        .sigs-row { display: table-row; }
        .sigs-cell {
            display: table-cell;
            width: 50%;
            text-align: center;
            vertical-align: top;
        }
        .sig-space { height: 22mm; }
        .sig-line {
            width: 65%;
            margin: 0 auto;
            border-bottom: 1px solid #475569;
            margin-bottom: 2mm;
        }
        .sig-name { font-weight: 700; color: #0f172a; }
        .sig-title { font-size: 8.5pt; color: #64748b; }
    </style>
</head>
<body>

    <div class="cover-page">
        <div class="cover-hero">
            <div class="cover-title">MASTER SERVICE OF AGREEMENT</div>
            <div class="cover-subtitle">No. Invoice: INV-TOS/2026/001</div>
        </div>
        
        <div style="padding: 5mm 0;">
            <div class="cover-accent-line"></div>
            <p style="font-size: 11pt; color: #475569; max-width: 90%;">
                Dokumen Perjanjian Induk dan Ketentuan Layanan ini mengikat secara hukum antara Penyedia Jasa (Worker) dan Pengguna Jasa (Client). Cakupan mencakup kesepakatan finansial, manajemen hak cipta, kepemilikan aset digital, serta klausul legalitas berdasarkan perundang-undangan Republik Indonesia.
            </p>

            <div class="cover-meta-container">
                <div class="cover-meta-row">
                    <div class="cover-meta-cell">
                        <div class="meta-label">Pihak Pertama (Worker)</div>
                        <div class="meta-value">Nakaa</div>
                        <div style="font-size: 9pt; color: #64748b; margin-top: 0.5mm;">Professional UI, Concept & System Developer</div>
                    </div>
                    <div class="cover-meta-cell">
                        <div class="meta-label">Pihak Kedua (Client)</div>
                        <div class="meta-value">Mitra / Pengguna Jasa</div>
                        <div style="font-size: 9pt; color: #64748b; margin-top: 0.5mm;">Entitas Pemesan Sistem</div>
                    </div>
                </div>
                <div class="cover-meta-row">
                    <div class="cover-meta-cell">
                        <div class="meta-label">Tanggal Efektif Kontrak</div>
                        <div class="meta-value">19 Juni 2026</div>
                    </div>
                    <div class="cover-meta-cell">
                        <div class="meta-label">Klasifikasi Dokumen</div>
                        <div class="meta-value" style="color: #0284c7;">Confidential / Perjanjian Hukum</div>
                    </div>
                </div>
            </div>
        </div>
    </div>


    <div class="invoice-section">
        <h1>FAKTUR TAGIHAN / INVOICE</h1>
        
        <div class="invoice-top-table">
            <div class="invoice-top-row">
                <div class="invoice-top-cell">
                    <div style="font-size: 14pt; font-weight: 800; color: #0f172a; letter-spacing: -0.2px;">NAKAA DESIGN & DEVELOPMENT</div>
                    <div style="font-size: 8.5pt; color: #64748b; margin-top: 1mm; line-height: 1.4;">
                        High-Fidelity UI/UX & Pemrograman Sistem Modular<br>
                        Hubungan Hukum & Kontrak Digital | Nomor: INV-TOS/2026/001
                    </div>
                </div>
                <div class="invoice-top-cell text-right" style="font-size: 9.5pt; color: #334155;">
                    <span class="font-bold" style="color: #0f172a;">Diterbitkan Untuk:</span><br>
                    Klien / Pemesan Jasa<br>
                    Tanggal Terbit: 19 Juni 2026<br>
                    Status: Menunggu Pembayaran Awal (DP)
                </div>
            </div>
        </div>

        <h2>1. Rincian Pengembangan Sistem</h2>
        <table class="premium-table">
            <thead>
                <tr>
                    <th style="width: 5%;" class="text-center">No</th>
                    <th style="width: 55%;">Deskripsi Pekerjaan Pemrograman</th>
                    <th style="width: 15%;" class="text-center">Paket Aset</th>
                    <th style="width: 25%;" class="text-right">Nilai Kontrak</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="text-center">1</td>
                    <td>
                        <span class="font-bold" style="color: #0f172a;">Jasa Pengembangan Aplikasi & Rekayasa Perangkat Lunak</span><br>
                        <span style="font-size: 8.5pt; color: #64748b;">
                            Mencakup pembuatan arsitektur modular, manajemen state/data store aman, validasi remote event/networking, serta integrasi aset visual performa tinggi.
                        </span>
                    </td>
                    <td class="text-center font-bold" style="color: #0284c7;">Packages 3<br><span style="font-size: 7.5pt; font-weight: normal; color: #64748b;">Commercial Use</span></td>
                    <td class="text-right font-bold">[Nilai Kontrak]</td>
                </tr>
            </tbody>
        </table>

        <h2>2. Struktur Pembayaran Termin (Milestone)</h2>
        <p style="font-size: 9.5pt;">Mekanisme pembiayaan wajib diselesaikan berdasarkan ketentuan pembagian 50% di awal dan 50% di akhir proyek:</p>
        
        <table class="premium-table">
            <thead>
                <tr>
                    <th style="width: 30%;">Tahapan Pembayaran</th>
                    <th style="width: 20%;" class="text-center">Persentase</th>
                    <th style="width: 50%;">Kondisi Penyerahan & Pekerjaan</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="font-bold">Termin I (Down Payment)</td>
                    <td class="text-center font-bold" style="color: #0284c7;">50%</td>
                    <td>Wajib diselesaikan di awal sebagai syarat mutlak dimulainya proses analisis kebutuhan dan penulisan baris kode pertama oleh Worker.</td>
                </tr>
                <tr>
                    <td class="font-bold">Termin II (Final Payment)</td>
                    <td class="text-center font-bold" style="color: #0284c7;">50%</td>
                    <td>Wajib dilunasi setelah seluruh sistem selesai dikembangkan, diuji bersama, dan dilakukan tepat sebelum penyerahan hak akses/arsitektur utuh kepada Klien.</td>
                </tr>
            </tbody>
        </table>

        <div class="summary-wrapper">
            <div class="summary-row">
                <div class="summary-left"></div>
                <div class="summary-right">
                    <table class="summary-block">
                        <tr>
                            <td>Subtotal Jasa Pemrograman</td>
                            <td class="text-right">[Nilai Kontrak]</td>
                        </tr>
                        <tr>
                            <td class="font-bold">Termin I: Pembayaran Awal (50%)</td>
                            <td class="text-right font-bold" style="color: #0284c7;">[50% Kontrak]</td>
                        </tr>
                        <tr>
                            <td class="font-bold">Termin II: Pelunasan Akhir (50%)</td>
                            <td class="text-right font-bold" style="color: #0284c7;">[50% Kontrak]</td>
                        </tr>
                        <tr class="grand-total">
                            <td>Total Nilai Kesepakatan (Net)</td>
                            <td class="text-right">[Nilai Kontrak]</td>
                        </tr>
                    </table>
                </div>
            </div>
        </div>

        <div style="margin-top: 12mm; font-size: 8.5pt; color: #64748b; border-top: 1px dashed #cbd5e1; padding-top: 3mm; line-height: 1.4;">
            <span class="font-bold" style="color: #475569;">Ketentuan Keabsahan Finansial:</span> Pembayaran hanya diakui sah melalui kanal transfer rekening resmi yang disetujui. Kegagalan pembayaran Termin II memberikan hak penuh kepada Worker untuk membekukan lisensi sistem operasional.
        </div>
    </div>


    <div>
        <h1>TERM OF SERVICE (KETENTUAN LAYANAN)</h1>
        
        <p>
            Syarat dan ketentuan ini mengatur tata cara kerja, batasan hukum, serta perlindungan hak cipta antara <strong>Worker (Nakaa)</strong> dan <strong>Klien</strong>. Penandatanganan dokumen ini menandakan persetujuan penuh terhadap seluruh pasal di bawah ini.
        </p>

        <h2>Pasal 1: Kebijakan Klasifikasi Hak Aset & Hak Milik Intelektual</h2>
        <p>
            Hak kekayaan intelektual atas baris kode, arsitektur data, dan aset sistem dikelompokkan menjadi 3 (tiga) skema paket operasional yang mengikat:
        </p>

        <div class="package-card">
            <div class="package-badge">Paket Terkunci</div>
            <div class="package-name">Packages 1 : Encrypted, Licensed</div>
            <p style="margin-bottom: 0; font-size: 9.5pt;">
                Seluruh kode sumber (source code) bersifat rahasia dan dienkripsi penuh oleh Worker. Klien hanya menerima hak guna pakai (runtime license). Klien dilarang keras membuka enkripsi, merekayasa balik (reverse engineering), menyalin, atau mendistribusikan kode tanpa persetujuan tertulis dari Worker. Hak kepemilikan aset mutlak milik Worker.
            </p>
        </div>

        <div class="package-card">
            <div class="package-badge">Paket Terbatas</div>
            <div class="package-name">Packages 2 : Open Source, Licensed</div>
            <p style="margin-bottom: 0; font-size: 9.5pt;">
                Klien memperoleh akses penuh terhadap kode sumber dalam keadaan terbuka untuk kebutuhan modifikasi dan pengembangan internal secara mandiri. Namun, aset dan kode tersebut <strong>TIDAK BISA/TIDAK BOLEH diperjualbelikan kembali</strong> kepada pihak ketiga. Hak kepemilikan aset dasar dan hak cipta tetap berada secara mutlak di tangan Pembuat (Worker).
            </p>
        </div>

        <div class="package-card">
            <div class="package-badge">Paket Komersial Penuh</div>
            <div class="package-name">Packages 3 : Open Source, Unlicensed, Commercial Use</div>
            <p style="margin-bottom: 0; font-size: 9.5pt;">
                Klien mendapatkan akses penuh terhadap seluruh baris kode tanpa enkripsi serta dibebaskan dari restriksi lisensi operasional. Klien memegang hak penuh untuk melakukan komersialisasi, penggandaan, serta <strong>bisa diperjualbelikan kembali secara bebas kepada pihak lain</strong>. Hak aset dan hak cipta beralih secara penuh dan mutlak menjadi milik Pembeli (Klien) setelah pelunasan kontrak dilakukan.
            </p>
        </div>

        <h2>Pasal 2: Ketentuan Pembayaran Pembagian 50/50</h2>
        <ol>
            <li><strong>Pembayaran Awal (50%):</strong> Klien wajib menyetorkan dana sebesar 50% dari nilai kontrak sebelum pekerjaan dimulai. Dana ini berfungsi sebagai tanda komitmen dan biaya operasional awal riset sistem.</li>
            <li><strong>Pembayaran Akhir (50%):</strong> Pelunasan sisa 50% wajib dibayarkan Klien setelah peninjauan fungsionalitas sistem dinyatakan selesai dan sebelum seluruh source code atau hak akses administratif dipindahtangankan.</li>
        </ol>

        <h2>Pasal 3: Pelanggaran Hak Cipta dan Sanksi Hukum Positif Indonesia</h2>
        <p>
            Tindakan penyalahgunaan aset, pendistribusian tanpa hak pada skema Paket 1 dan Paket 2, serta klaim sepihak atas ciptaan milik Worker merupakan bentuk pelanggaran hukum serius dan akan diproses melalui jalur pidana maupun perdata.
        </p>

        <div class="legal-warning-box">
            <h3>PERINGATAN ATAS PELANGGARAN HAK CIPTA (UU NO. 28 TAHUN 2014)</h3>
            <p>
                Berdasarkan <strong>Undang-Undang Republik Indonesia Nomor 28 Tahun 2014 tentang Hak Cipta</strong>, program komputer dan database adalah ciptaan yang dilindungi (Pasal 40 ayat 1). Pelanggaran terhadap hak ekonomi pencipta dikenakan sanksi pidana:
            </p>
            <ul style="margin-top: 1.5mm; margin-bottom: 0; color: #7f1d1d; font-size: 9pt;">
                <li><strong>Pasal 113 Ayat (3):</strong> Setiap orang yang tanpa hak dan/atau tanpa izin melakukan pelanggaran hak ekonomi untuk penggunaan secara komersial dipidana dengan pidana penjara paling lama 4 (empat) tahun dan/atau denda paling banyak Rp1.000.000.000,00 (satu miliar rupiah).</li>
                <li><strong>Pasal 113 Ayat (4):</strong> Pelanggaran yang dilakukan dalam bentuk pembajakan dipidana dengan pidana penjara paling lama 10 (sepuluh) tahun dan/atau pidana denda paling banyak Rp4.000.000.000,00 (empat miliar rupiah).</li>
            </ul>
        </div>
        
        <p>
            Worker akan menuntut ganti rugi materil melalui Pengadilan Niaga serta melakukan pelaporan pidana ke Direktorat Tindak Pidana Siber Bareskrim Polri jika ditemukan kebocoran aset kode pada paket berlisensi terbatas.
        </p>

        <h2>Pasal 4: Hukum yang Berlaku & Penyelesaian Perselisihan</h2>
        <ol>
            <li>Perjanjian ini diatur, ditafsirkan, dan tunduk sepenuhnya pada hukum Negara Kesatuan Republik Indonesia.</li>
            <li>Segala sengketa yang timbul akibat pelaksanaan kontrak ini akan diselesaikan secara musyawarah untuk mufakat dalam waktu maksimal 30 hari.</li>
            <li>Jika musyawarah gagal, Kedua Belah Pihak sepakat memilih domisili hukum yang tetap di Pengadilan Negeri wilayah tempat tinggal/domisili Worker.</li>
        </ol>

        <div class="signatures-container">
            <h2>Persetujuan Para Pihak</h2>
            <p style="font-size: 9pt; color: #475569;">
                Kedua belah pihak dengan ini menandatangani Master Service of Agreement ini sebagai bukti kesepakatan mutlak tanpa adanya paksaan dari pihak manapun.
            </p>
            
            <div class="sigs-table">
                <div class="sigs-row">
                    <div class="sigs-cell">
                        <div class="sig-title font-bold" style="color:#0f172a; margin-bottom: 4mm;">PIHAK PERTAMA<br>(Penyedia Jasa / Worker)</div>
                        <div class="sig-space"></div>
                        <div class="sig-line"></div>
                        <div class="sig-name">Nakaa</div>
                        <div class="sig-title">Professional Developer & UI/UX Designer</div>
                    </div>
                    <div class="sigs-cell">
                        <div class="sig-title font-bold" style="color:#0f172a; margin-bottom: 4mm;">PIHAK KEDUA<br>(Pengguna Jasa / Klien)</div>
                        <div class="sig-space"></div>
                        <div class="sig-line"></div>
                        <div class="sig-name">......................................................</div>
                        <div class="sig-title">Klien / Perwakilan Sah Perusahaan</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

</body>
</html>
"""

with open("master_service_agreement.html", "w", encoding="utf-8") as f:
    f.write(html_content)

HTML("master_service_agreement.html").write_pdf("invoice_and_tos-v2.pdf")
print("PDF v2 generated successfully.")