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
        'Kondisi': 'Baik',
        'Nama Barang1': 'Desktop',
        'Merk1': 'Dell',
        'Tipe1': '3010',
        'Nomor Seri1': '00073563',
        'Kondisi1': 'Baik'
    }
    report = ReportAdHoc(
        name='sample_report',
        title=title,
        sub_title=sub_title,
        detail=detail,
        receiver='Nugraha Dila Prawisda',
        sender='Iman Utomo',
        equipment=['Ban Cadangan', 'Spion kanan-kiri & dalam', 'Dongkrak + handle'],
        add_equipment=['STNK Asli', 'Radio, AC', 'Buku BPKB']
    )
    return report.write_pdf_view()
