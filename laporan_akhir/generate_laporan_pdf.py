"""Generate a concise, evidence-based PDF report for the reference project."""
from pathlib import Path
import json

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulation"
OUT = Path(__file__).resolve().parent / "Laporan_Proyek_Referensi.pdf"


def p(text, style):
    return Paragraph(text, style)


def section(title, styles):
    return [Spacer(1, 0.22 * cm), p(title, styles["Heading2"]), Spacer(1, 0.08 * cm)]


def table(rows, widths=None):
    t = Table(rows, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17365D")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("LEADING", (0, 0), (-1, -1), 11),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#B7C9D6")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#EDF3F7")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#52616B"))
    canvas.drawString(2.0 * cm, 1.15 * cm, "TEKDAS Students | Laporan proyek referensi")
    canvas.drawRightString(19.0 * cm, 1.15 * cm, f"Halaman {doc.page}")
    canvas.restoreState()


def main():
    metrics = json.loads((SIM / "model_metrics.json").read_text(encoding="utf-8"))
    quality = json.loads((SIM / "data_quality_report.json").read_text(encoding="utf-8"))
    importance = pd.read_csv(SIM / "feature_importance.csv").head(10)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="TitleReport", parent=styles["Title"], fontName="Helvetica-Bold",
                              fontSize=21, leading=26, textColor=colors.HexColor("#17365D"), alignment=TA_CENTER))
    styles.add(ParagraphStyle(name="SubTitle", parent=styles["Normal"], fontSize=11, leading=15,
                              textColor=colors.HexColor("#52616B"), alignment=TA_CENTER))
    styles["BodyText"].fontSize = 9.5
    styles["BodyText"].leading = 14
    styles["BodyText"].alignment = TA_JUSTIFY
    styles["Heading2"].fontName = "Helvetica-Bold"
    styles["Heading2"].fontSize = 13
    styles["Heading2"].leading = 17
    styles["Heading2"].textColor = colors.HexColor("#17365D")

    story = [Spacer(1, 2.2 * cm), p("LAPORAN PROYEK TEKNOLOGI CERDAS", styles["TitleReport"]),
             Spacer(1, 0.25 * cm), p("Prediksi Customer Churn: Business Intelligence, Machine Learning, dan LLM Analyst", styles["SubTitle"]),
             Spacer(1, 1.0 * cm)]
    story += [table([
        ["Komponen", "Keterangan"],
        ["Status", "Proyek referensi / track reproduce"],
        ["Ruang lingkup", "Dataset e-commerce yang dibundel di repository; dashboard Streamlit; Random Forest; Ollama LLM"],
        ["Unit prediksi", "Satu pelanggan dengan label churned (0/1)"],
        ["Snapshot data", quality["snapshot_date"]],
        ["Penyusun", "Belum diisi - lengkapi identitas mahasiswa sebelum penyerahan"],
    ], [4.0 * cm, 13.5 * cm]), Spacer(1, 0.7 * cm),
        p("Ringkasan eksekutif", styles["Heading2"]),
        p("Proyek ini membangun alur data-ke-keputusan untuk membantu manajer retensi mengidentifikasi pelanggan yang berisiko churn. Data pelanggan dan transaksi divalidasi, diringkas sebagai business intelligence, lalu dipakai oleh model klasifikasi. Skor model dan bukti transaksi diteruskan ke LLM lokal hanya untuk menyusun rekomendasi berbasis evidence. Pada test set 1.600 pelanggan, Random Forest mencapai ROC-AUC 0,733 dan F1 churn 0,387 pada threshold 0,50. Hasil ini berguna sebagai demonstrasi pembelajaran, tetapi belum cukup untuk keputusan otomatis atau klaim kausal.", styles["BodyText"]),
        Spacer(1, 0.25 * cm), p("Kata kunci: customer churn; business intelligence; Random Forest; Streamlit; Ollama; grounded LLM.", styles["BodyText"]), PageBreak()]

    story += section("1. Masalah, tujuan, dan kontribusi", styles)
    story += [p("Churn pelanggan dapat mengurangi pendapatan berulang, sementara tim retensi perlu memprioritaskan pelanggan dengan sumber daya terbatas. Dashboard deskriptif saja tidak memberi urutan risiko individual; sebaliknya skor model tanpa konteks sulit ditindaklanjuti. Sistem ini menggabungkan keduanya: BI menjelaskan kondisi agregat, ML mengestimasi probabilitas churn, dan LLM mengubah evidence yang diberikan menjadi saran singkat untuk manajer.", styles["BodyText"]),
              Spacer(1, 0.12 * cm),
              table([["Pertanyaan", "Jawaban/evidence dalam proyek"],
                     ["RQ1 - Seberapa baik prediksi churn?", "Dievaluasi pada hold-out test set dengan precision, recall, F1, ROC-AUC, dan confusion matrix."],
                     ["RQ2 - Apa dampak threshold?", "Dibandingkan pada 0,30; 0,50; dan 0,70 untuk memperlihatkan trade-off false positive dan false negative."],
                     ["RQ3 - Apa peran LLM?", "Mengkomunikasikan profil, pesanan terakhir, probabilitas ML, dan faktor global; prompt melarang fakta atau motif yang tidak tersedia."],
                     ["Kontribusi", "Implementasi referensi end-to-end yang dapat direproduksi, bukan proyek adaptasi/orisinal."]], [5.2 * cm, 12.3 * cm])]
    story += section("2. Data dan kualitas", styles)
    story += [p("Repository tidak mendokumentasikan URL, lisensi, atau pemilik asli dataset. Karena itu laporan ini menyebutnya sebagai data e-commerce pembelajaran yang dibundel, bukan mengklaim provenance Kaggle tertentu. Sebelum penggunaan di luar kelas, provenance, izin, periode pengumpulan, dan kebijakan privasi wajib diverifikasi.", styles["BodyText"]), Spacer(1, 0.12 * cm),
              table([["Tabel", "Unit", "Jumlah", "Peran"],
                     ["customers.csv", "pelanggan", f"{quality['customers_rows']:,}", "target churn dan fitur pelanggan"],
                     ["orders.csv", "pesanan", f"{quality['orders_rows']:,}", "evidence transaksi dan return"],
                     ["product_summary.csv", "produk", f"{quality['products_rows']:,}", "ringkasan BI produk"],
                     ["monthly_revenue.csv", "bulan", f"{quality['monthly_rows']:,}", "tren revenue delivered"]], [4.0 * cm, 3.4 * cm, 2.1 * cm, 8.0 * cm]), Spacer(1, 0.13 * cm),
              table([["Pemeriksaan", "Hasil", "Implikasi"],
                     ["Prevalensi churn", f"{quality['customer_churn_rate_pct']:.2f}%", "Kelas minoritas; accuracy bukan metrik tunggal."],
                     ["Rating pesanan missing", f"{quality['orders_missing_rating_pct']:.1f}%", "Rating perlu diperlakukan hati-hati pada analisis transaksi."],
                     ["Return rate pesanan", f"{quality['order_return_rate_pct']:.2f}%", "Gunakan orders.csv untuk analisis return."],
                     ["return_rate bulanan", "0 untuk semua bulan", "Agregat bulanan hanya merepresentasikan order Delivered; tidak valid untuk menyimpulkan return."],
                     ["Konsistensi agregat", "Lolos", "Revenue produk cocok dengan non-cancelled; revenue bulanan cocok dengan delivered revenue."]], [4.0 * cm, 3.3 * cm, 10.2 * cm]), PageBreak()]

    story += section("3. Metode dan arsitektur", styles)
    story += [p("Alur sistem: CSV sumber -> validasi dan cleaning -> feature engineering -> BI dashboard + pipeline ML -> probabilitas churn -> evidence pelanggan/pesanan + faktor model -> Ollama LLM -> rekomendasi untuk pengguna. LLM tidak mengubah skor model dan tidak diberi akses ke data di luar evidence yang dirangkai aplikasi.", styles["BodyText"]), Spacer(1, 0.14 * cm),
              table([["Tahap", "Implementasi"],
                     ["Validasi", "Memeriksa kolom wajib pada empat CSV serta semantik agregasi."],
                     ["Feature engineering", "Tenure pelanggan, orders per year, reviews per order, dan returns per order; total 21 fitur sebelum one-hot encoding."],
                     ["Split", "Stratified hold-out 80:20, random_state=42; train 6.400 dan test 1.600 pelanggan."],
                     ["Preprocessing", "Median imputation numerik; most-frequent imputation kategorikal; OneHotEncoder(handle_unknown=ignore) di dalam pipeline untuk membatasi leakage preprocessing."],
                     ["Model", "RandomForestClassifier: 350 trees, min_samples_leaf=3, class_weight=balanced, random_state=42."],
                     ["LLM", "Ollama model default llama3.2, temperature 0,2; prompt menyatakan skor bukan kausalitas dan melarang penambahan fakta."],
                     ["Aplikasi", "Streamlit: data, BI, prediksi dengan threshold interaktif, dan analyst LLM."]], [4.3 * cm, 13.2 * cm])]
    story += section("4. Desain evaluasi", styles)
    story += [p("Model dievaluasi pada test set yang tidak digunakan untuk fitting. Karena churn hanya sekitar 9%, F1, precision, recall, dan ROC-AUC dilaporkan bersama accuracy. Baseline naif yang selalu memprediksi tidak churn akan memperoleh accuracy kira-kira 91,1% pada distribusi test, tetapi recall dan F1 churn 0; ini menunjukkan mengapa accuracy tinggi tidak cukup untuk tujuan retensi.", styles["BodyText"]), Spacer(1, 0.1 * cm),
              p("Evaluasi LLM pada repository ini masih bersifat pemeriksaan prompt dan demo runtime, bukan studi pengguna terstruktur. Oleh sebab itu, laporan tidak mengklaim tingkat konsistensi LLM secara kuantitatif.", styles["BodyText"]), PageBreak()]

    story += section("5. Hasil", styles)
    story += [table([["Metrik test set", "Nilai"],
                     ["Accuracy", f"{metrics['accuracy']:.3f}"], ["Precision churn", f"{metrics['precision_churn']:.3f}"],
                     ["Recall churn", f"{metrics['recall_churn']:.3f}"], ["F1 churn", f"{metrics['f1_churn']:.3f}"],
                     ["ROC-AUC", f"{metrics['roc_auc']:.3f}"], ["Churn rate test", f"{metrics['test_churn_rate']:.3f}"]], [7.0 * cm, 4.0 * cm]), Spacer(1, 0.18 * cm),
              p("Pada threshold 0,50, confusion matrix adalah TN=1.312, FP=145, FN=74, TP=69. Dengan demikian, model menangkap 69 dari 143 pelanggan churn pada test set, tetapi juga menandai 145 pelanggan non-churn. Threshold harus dipilih berdasarkan biaya intervensi dan biaya kehilangan pelanggan, bukan hanya satu skor agregat.", styles["BodyText"]), Spacer(1, 0.15 * cm),
              table([["Threshold", "Precision", "Recall", "F1", "FP", "FN"],
                     ["0,30", "0,270", "0,601", "0,372", "233", "57"],
                     ["0,50", "0,322", "0,483", "0,387", "145", "74"],
                     ["0,70", "0,414", "0,084", "0,140", "17", "131"]], [2.5*cm, 2.5*cm, 2.5*cm, 2.0*cm, 2.0*cm, 2.0*cm]), Spacer(1, 0.18*cm),
              p("Threshold 0,30 menangkap lebih banyak churn namun memperbesar daftar kontak; threshold 0,70 menghasilkan presisi lebih tinggi tetapi melewatkan hampir semua churn. Pada metrik F1, 0,50 adalah yang terbaik dari tiga threshold yang diperiksa.", styles["BodyText"])]
    fi_rows = [["Fitur global", "Importance"]] + [[str(r.feature).replace("num__", "").replace("cat__", ""), f"{r.importance:.3f}"] for r in importance.itertuples()]
    story += section("6. Interpretasi model", styles) + [p("Feature importance Random Forest adalah kontribusi prediktif global, bukan bukti sebab-akibat untuk individu. Faktor teratas terutama berkaitan dengan recency, volume, dan nilai belanja.", styles["BodyText"]), Spacer(1, 0.1*cm), table(fi_rows, [10.5*cm, 3.0*cm]), PageBreak()]

    story += section("7. Diskusi, etika, dan keterbatasan", styles)
    story += [p("Model menunjukkan kemampuan pemisahan moderat (ROC-AUC 0,733), tetapi precision 0,322 berarti sebagian besar pelanggan yang ditandai belum tentu churn. Rekomendasi yang aman adalah menggunakan skor sebagai prioritisasi untuk outreach yang proporsional, dengan keputusan akhir tetap pada manusia. Jangan gunakan prediksi sebagai alasan untuk memperlakukan pelanggan secara diskriminatif.", styles["BodyText"]), Spacer(1, 0.1*cm),
              table([["Risiko/keterbatasan", "Mitigasi atau konsekuensi"],
                     ["Provenance dan lisensi tidak tercatat", "Tidak boleh diasumsikan layak untuk produksi; verifikasi sumber dan izin terlebih dahulu."],
                     ["Label historis bukan kausalitas", "Jangan menyebut faktor model sebagai penyebab churn; lakukan eksperimen retensi terkontrol."],
                     ["Bias dan representativitas tidak dievaluasi", "Audit per kelompok yang sah dan minimalkan penggunaan atribut sensitif."],
                     ["Drift dan kalibrasi belum diuji", "Pantau performa setelah deployment dan retrain hanya dengan governance yang jelas."],
                     ["LLM dapat menghasilkan klaim tak didukung", "Grounding, prompt inspection, human review, logging, dan evaluasi kasus uji diperlukan."],
                     ["Data pelanggan berpotensi pribadi", "Batasi akses, minimalkan data pada prompt, dan patuhi kebijakan retensi/privasi."]], [6.2*cm, 11.3*cm])]
    story += section("8. Kesimpulan dan reproduksibilitas", styles)
    story += [p("(1) Pipeline referensi berhasil menghubungkan BI, prediksi churn, dan komunikasi berbantuan LLM. (2) Pada hold-out test set, Random Forest mencapai ROC-AUC 0,733 dan F1 churn 0,387 pada threshold 0,50. (3) Ambang keputusan mengubah trade-off operasional secara nyata. (4) LLM diposisikan sebagai pembantu komunikasi evidence, bukan pembuat keputusan atau penjelas kausal. (5) Data dan evaluasi saat ini mendukung pembelajaran/reproduce, bukan deployment produksi.", styles["BodyText"]), Spacer(1, 0.15*cm),
              p("Untuk menjalankan ulang dari folder simulation: <font name='Courier'>pip install -r requirements.txt</font>, kemudian <font name='Courier'>python data_prep.py</font>, <font name='Courier'>python ml_model.py</font>, dan <font name='Courier'>streamlit run app.py</font>. Untuk LLM, jalankan <font name='Courier'>ollama serve</font>, unduh model llama3.2, lalu gunakan <font name='Courier'>python vai_analyst.py</font>. PDF ini dibuat dari artefak yang ada pada repository dan tidak menggantikan verifikasi data atau evaluasi pengguna nyata.", styles["BodyText"]), Spacer(1, 0.25*cm),
              p("Catatan pengungkapan AI: laporan ini disusun dengan bantuan AI berbasis kode, lalu angka dan klaimnya ditautkan ke file data_quality_report.json, model_metrics.json, feature_importance.csv, serta implementasi pipeline pada repository.", styles["BodyText"])]

    doc = SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=1.8*cm, bottomMargin=1.8*cm,
                            title="Laporan Proyek Teknologi Cerdas - Customer Churn")
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(OUT)


if __name__ == "__main__":
    main()
