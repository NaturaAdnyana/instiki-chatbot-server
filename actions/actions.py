from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

import gspread

gc = gspread.service_account(filename='actions/auth/instiki-chatbot-76f64c09367a.json')
sh = gc.open_by_key('1rWWwcRA3xmdflMPAiC5SHUs_w1Tp23tSwzwFIoV6h80')
worksheet = sh.worksheet("MAHASISWA")

def get_user_data(nim):
    cell_list = worksheet.find(nim)
    values_list = worksheet.row_values(cell_list.row)
    headers = worksheet.row_values(1)
    record = dict(zip(headers, values_list))
    
    return record

class ActionGetNamaNim(Action):
    def name(self) -> Text:
        return "action_get_nama_nim"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        nama = next(tracker.get_latest_entity_values("nama"), None)
        nim = next(tracker.get_latest_entity_values("nim"), None)

        if nim:
            try:
                cell_list = worksheet.find(nim)
                if cell_list and nama:
                    dispatcher.utter_message(response="utter_nama_nim", nama=nama, nim=nim)
                    dispatcher.utter_message(response="utter_menawarkan_bantuan_mhs")
                elif cell_list:
                    dispatcher.utter_message(response="utter_nim_only", nim=nim)
                    dispatcher.utter_message(response="utter_menawarkan_bantuan_mhs")
                else:
                    dispatcher.utter_message(response="utter_data_tidak_cocok", nim=nim)
            except Exception as e:
                dispatcher.utter_message(text="Mohon maaf, saat ini IQA mengalami gangguan, mohon doanya agar bisa segera pulih 🥲🙏")
                dispatcher.utter_message(text="Jika membutuhkan informasi segera, silahkan menghubungi Information Center kami: https://wa.me/6281339822383")

        elif nama:
            dispatcher.utter_message(response="utter_nama_only", nama=nama)
            dispatcher.utter_message(response="utter_menawarkan_bantuan")

        else:
            dispatcher.utter_message(text="Halo, kami siap memperkenalkan anda tentang INSTIKI.")
            dispatcher.utter_message(text="utter_menawarkan_bantuan")

        return [SlotSet("nama", nama), SlotSet("nim", nim)]

class ActionGetRekomendasiMatkul(Action):
    def name(self) -> Text:
        return "action_get_rekomendasi_matkul"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        nim = tracker.get_slot('nim')

        if not nim:
            dispatcher.utter_message(response="utter_cegah_guest")
            return []

        try:
            record = get_user_data(nim)
            jurusan = record.get('JURUSAN')

            if jurusan == "MDI":
                dispatcher.utter_message(response="utter_matkul_mdi")
            elif jurusan == "SK":
                dispatcher.utter_message(response="utter_matkul_kab")
            elif jurusan == "TIP":
                dispatcher.utter_message(response="utter_matkul_tip")
            elif jurusan == "BD":
                dispatcher.utter_message(response="utter_matkul_bd")
            elif jurusan == "DKV":
                dispatcher.utter_message(response="utter_matkul_dkv")
            elif jurusan == "SK":
                dispatcher.utter_message(response="utter_matkul_sk")
            else:
                dispatcher.utter_message(text="Mohon maaf, ada kesalahan dalam data kamu, mohon hubungi Information Center kami: https://wa.me/6281339822383")

        except Exception as e:
            dispatcher.utter_message(text="Mohon maaf, saat ini IQA mengalami gangguan, mohon doanya agar bisa segera pulih 🥲🙏")
            dispatcher.utter_message(text="Jika membutuhkan informasi segera, silahkan menghubungi Information Center kami: https://wa.me/6281339822383")
        return []

class ActionGetBiayaKRS(Action):
    def name(self) -> Text:
        return "action_get_biaya_krs"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        nim = tracker.get_slot('nim')
        if not nim:
            dispatcher.utter_message(response="utter_cegah_guest")
            return []

        try:
            record = get_user_data(nim)
            status_krs = record.get('STATUS KRS')
            nominal_krs = "{:,}".format(int(record.get('BIAYA KRS')))
            tunggakan_krs = "{:,}".format(int(record.get('SISA TUNGGAKAN')))

            if status_krs == "Lunas":
                dispatcher.utter_message(response="utter_krs_lunas", nominal_krs=nominal_krs)
            elif status_krs == "Belum Lunas":
                dispatcher.utter_message(response="utter_krs_belum_lunas", nominal_krs=nominal_krs, tunggakan_krs=tunggakan_krs)
            else:
                dispatcher.utter_message(text="Mohon maaf, ada kesalahan dalam data kamu, mohon hubungi Information Center kami: https://wa.me/6281339822383")

        except Exception as e:
            dispatcher.utter_message(text="Mohon maaf, saat ini IQA mengalami gangguan, mohon doanya agar bisa segera pulih 🥲🙏")
            dispatcher.utter_message(text="Jika membutuhkan informasi segera, silahkan menghubungi Information Center kami: https://wa.me/6281339822383")
            print(e)
        return []

class ActionGetIPSaatIni(Action):
    def name(self) -> Text:
        return "action_get_ip_saat_ini"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        nim = tracker.get_slot('nim')

        if not nim:
            dispatcher.utter_message(response="utter_cegah_guest")
            return []

        try:
            record = get_user_data(nim)
            ipk = record.get('IP')

            dispatcher.utter_message(response="utter_ip_saat_ini", ipk=ipk)
            dispatcher.utter_message(text="Kesuksesan sejati juga ditentukan oleh keterampilan, pengalaman, jaringan, dan sikap positif yang kamu kembangkan sepanjang perjalananmu. Tetaplah belajar, teruslah berkembang, dan jangan ragu untuk mengambil peluang yang ada di depanmu.")

        except Exception as e:
            dispatcher.utter_message(text="Mohon maaf, saat ini IQA mengalami gangguan, mohon doanya agar bisa segera pulih 🥲🙏")
            dispatcher.utter_message(text="Jika membutuhkan informasi segera, silahkan menghubungi Information Center kami: https://wa.me/6281339822383")
            print(e)
        return []

class ActionGetSKSSaatIni(Action):
    def name(self) -> Text:
        return "action_get_sks_saat_ini"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        nim = tracker.get_slot('nim')
        syarat_sks_wajib = 135
        syarat_sks_pilihan = 9
        if not nim:
            dispatcher.utter_message(response="utter_cegah_guest")
            return []

        try:
            record = get_user_data(nim)
            sks_wajib = record.get('TOTAL SKS WAJIB')
            sks_pilihan = record.get('TOTAL SKS PILIHAN')

            if int(sks_wajib) >= syarat_sks_wajib and int(sks_pilihan) >= syarat_sks_pilihan:
                dispatcher.utter_message(response="utter_sks_telah_cukup", sks_wajib=sks_wajib, sks_pilihan=sks_pilihan)

            else:
                sks_wajib_sisa = max(syarat_sks_wajib - int(sks_wajib), 0)
                sks_pilihan_sisa = max(syarat_sks_pilihan - int(sks_pilihan), 0)
                jml_matkul_wajib = f"{int(sks_wajib_sisa)//3}-{int(sks_wajib_sisa)//2}"
                jml_matkul_pilihan = f"{int(sks_pilihan_sisa)//3}"

                dispatcher.utter_message(response="utter_sks_saat_ini", sks_wajib=sks_wajib, sks_pilihan=sks_pilihan)
                dispatcher.utter_message(response="utter_sks_sisa", sks_wajib_sisa=sks_wajib_sisa, sks_pilihan_sisa=sks_pilihan_sisa, jml_matkul_wajib=jml_matkul_wajib, jml_matkul_pilihan=jml_matkul_pilihan)

        except Exception as e:
            dispatcher.utter_message(text="Mohon maaf, saat ini IQA mengalami gangguan, mohon doanya agar bisa segera pulih 🥲🙏")
            dispatcher.utter_message(text="Jika membutuhkan informasi segera, silahkan menghubungi Information Center kami: https://wa.me/6281339822383")
            print(e)
        return []