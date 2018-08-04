from NA_Report.ad_hoc import ReportAdHoc


def create_ad_hoc(request):
    title = "Berita Acara Penyerahan Kendaraan"
    sub_title = """
    Telah diserahkan 1 Unit Kendaraan Operasional PT.NuFarm Indonesia
    kepada <b>Pak Nugraha Dila Prawisda</b> dengan uraian sebagai berikut:
    """
    detail = {
        'Nama Barang': 'Desktop',
        'Merk': 'Dell',
        'Tipe': '3010',
        'Nomor Seri': '00073563',
        'Kondisi': 'Baik'
    }
    report = ReportAdHoc(
        title=title,
        sub_title=sub_title,
        detail=detail
    )
    return report.write_pdf_view()