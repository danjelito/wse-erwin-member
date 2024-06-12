import pandas as pd
import numpy as np
import config

to_rename = {
    "date_of_birth": "dob",
    "from": "start_date",
    "to": "end_date",
    "fully_paid_date": "fp_date",
    "membership": "product",
    "home_center": "center",
    "partner_date_of_birth": "dob2",
    "partner_city": "city",
    "partner_gender": "gender",
    "partner_household_income": "income",
    "partner_job": "job1",
    "partner_occupation": "job2",
    "display_name": "name",
}
to_drop = [
    "external_id",
    "partner_industry",
    "partner_street2",
    "partner_age",
    "partner_hobby",
    "partner_interest",
    "dob2",
    "job1",
    "job2",
    "name",
    "index",
]
income_cat = pd.CategoricalDtype(
    [
        "Below Rp 10.000.000",
        "Rp 10.000.000 - Rp 20.000.000",
        "Rp 20.000.000 - Rp 30.000.000",
        "Rp 30.000.000 - Rp 40.000.000",
        "Above Rp 40.000.000",
    ],
    ordered=True,
)


def clean_col_name(col):
    return (
        col.lower()
        .replace("/display name", "")
        .replace("/month", "")
        .replace("position", "")
        .replace("?", "")
        .strip()
        .replace(" ", "_")
        .replace("/", "_")
        .replace("(", "")
        .replace(")", "")
        .replace("__", "_")
        .replace("followers_partners_", "")
        .strip()
    )


def clean_job(df_):
    return np.where(
        df_["job1"].isna(),
        df_["job2"].str.lower().str.replace("[^\w\s]", "", regex=True).str.strip(),
        df_["job1"].str.lower().str.replace("[^\w\s]", "", regex=True).str.strip(),
    )


def group_job(job_col):
    """Group job to entry level, middle level etc."""

    mask_staff = "staff|karyawan|employee|karyawan swasta|pekerja professional|pekerja profesional|associate|engineer|marketing|finance|intern|flight attendant|accounting|graphic designer|analyst|nurse|legal|secretary|programmer|sales|hr|civil servant|pr|tax officer|management trainee|content creator|researcher|designer|accountant|research assistant|web developer|customer support|risk management|photographer|human resources|business development|journalist|pharmacist|admin|purchaser|human resource|pengelola barang milik negara|pengawas junior|officer"
    mask_manager = "manager|director|supervisor|it|swasta|ceo|direktur|head|vp|gm"
    mask_other = "doctor|pns|consultant|teacher|dosen|lecturer|government servant|lawyer|pediatrician|dentist|police officer|dokter"
    mask_student = "student|sekolah|siswa|pelajar|high schooler|highschooler|stude|fresh grad"
    mask_college = "maha|mhs|college"
    mask_enterpreneur = "enterpreneur|businessman|businesswoman|owner|fresh graduate|pengusaha|entrepreneur|selfemployed|online shop|entrepeneur|wirausaha|bussiness woman"
    mask_not_working = "freshgraduate|tidak bekerja|job seeker|belum bekerja|freshgrad|freash graduate|graduated|not yet"
    mask_wife = "housewife|ibu rumah|house wife"
    mask_freelance = "freelance|free lance"

    conditions = [
        (job_col.str.lower().str.contains(mask_staff, na=False)),
        (job_col.str.lower().str.contains(mask_manager, na=False)),
        (job_col.str.lower().str.contains(mask_other, na=False)),
        (job_col.str.lower().str.contains(mask_student, na=False)),
        (job_col.str.lower().str.contains(mask_college, na=False)),
        (job_col.str.lower().str.contains(mask_not_working, na=False)),
        (job_col.str.lower().str.contains(mask_enterpreneur, na=False)),
        (job_col.str.lower().str.contains(mask_wife, na=False)),
        (job_col.str.lower().str.contains(mask_freelance, na=False)),
    ]
    choices = [
        "Employee - Entry Level",
        "Employee - Middle to Upper Level",
        "Employee - Other",
        "Student",
        "College Student",
        "Not Working",
        "Enterpreneur",
        "Housewife",
        "Freelance",
    ]
    return np.select(conditions, choices, default="Unidentified")


def clean_gender(gender_col):
    return gender_col.replace(False, "Not Specified").fillna("Not Specified")


def get_age(df_):
    """Get age between DOB and start_date, cast to np.nan if < 15 YO or > 65 YO."""
    result = (
        (df_["start_date"] - df_["dob"]).div(pd.Timedelta("365 days")).apply(np.floor)
    )
    return np.where(((result < 15) | (result > 65)), np.nan, result)


def get_membership_code(series):
    """Get membership code."""
    membership_code = pd.Series(series).str.extract("(\[.+\])")
    membership_code = (
        membership_code.iloc[:, 0]  # convert DF to series
        .str.replace("[", "", regex=False)
        .str.replace("]", "", regex=False)
        .str.replace(".", " ", regex=False)
        .str.replace("(\d+$)", "", regex=True)
        .str.strip()
    )
    return membership_code


def get_membership_duration(series):
    """Get membership duration."""
    membership_code = pd.Series(series).str.extract("(\[.+\])")
    membership_duration = (
        membership_code.iloc[:, 0]  # convert DF to series
        .str.replace("[", "", regex=False)
        .str.replace("]", "", regex=False)
        .str.replace(".", " ", regex=False)
        .str.extract("(\d+)")  # extract digit
    )
    return membership_duration


def is_active(
    df: pd.DataFrame,
    start_date_col: pd.Timestamp,
    end_date_col: pd.Timestamp,
    lower_bound: str,
):
    """
    Returns boolean to indicate if a member is active in a certain timeframe.
    By default, the timeframe is one month,
    starting from the lower_bound to the upper_bound
    and inclusive

    Arguments:
        df -- dataframe
        start_date -- contract start date of the member
        end_date -- contract end date of the member
        lower_bound -- lower bound of the timeframe

    Returns:
        boolean indicating if the member is active on the timeframe
    """

    lower_bound = pd.to_datetime(lower_bound)
    upper_bound = lower_bound + pd.offsets.MonthEnd(0)

    conditions = (
        ((df[start_date_col] <= lower_bound) & (df[end_date_col] >= upper_bound)),
        (
            (df[start_date_col] <= lower_bound)
            & (df[end_date_col] <= upper_bound)
            & (df[end_date_col] >= lower_bound)
        ),
        (
            (df[start_date_col] >= lower_bound)
            & (df[start_date_col] <= upper_bound)
            & (df[end_date_col] >= upper_bound)
        ),
        ((df[start_date_col] >= lower_bound) & (df[end_date_col] <= upper_bound)),
        True,
    )
    choices = [True, True, True, True, False]
    return np.select(conditions, choices, default=False)


def clean_center(df_: pd.DataFrame, center_col: str, is_cpt_col: str, core_product_col: str) -> pd.Series:
    """Get center.
    """

    conditions = [
        df_[is_cpt_col] == True,
        df_[core_product_col] == "Go",
        True,
    ]
    choices = [
        "Corporate",
        "Online Center",
        df_[center_col].str.upper().map(config.center_map),
    ]
    center = np.select(conditions, choices, "ERROR")
    return center


def clean_area(df_: pd.DataFrame) -> pd.Series:
    """Get area from center.

    :param pd.DataFrame df_: DF.
    :return pd.Series: area.
    """

    conditions = [
        df_["center"].isna(),
        df_["center"] == "Online Center",
        df_["center"] == "Corporate",
        df_["center"].isin(config.jkt_1),
        df_["center"].isin(config.jkt_2),
        df_["center"].isin(config.jkt_3),
        df_["center"].isin(config.bdg),
        df_["center"].isin(config.sby),
        df_["center"].isin(config.map_areas.get("Other")),
    ]
    choices = [
        "NONE",
        "Online Center",
        "Corporate",
        "JKT 1",
        "JKT 2",
        "JKT 3",
        "BDG",
        "SBY",
        "Other",
    ]
    area = np.select(conditions, choices, default="NONE")
    return area


def assert_cpt_catched(df):
    return np.where(
        df["product"].str.lower().str.contains("cpt|corporate|corp", regex=True),
        True,
        df["is_cpt"],
    )


def create_region(city_col, street_col):
    # mask
    mask_jabo = "jakarta|jkt|jkarta|jakut|jaksel|jakbar|jaktim|bogor|bgor|bogr|depok|dpk|tangerang|tgrg|bekasi|bks|kuningan|scbd|karawang|setiabudi|tanggerang|cikarang|cakung|tebet|bintaro|gunung putri|mampang|cilandak|tanah abang|pasar minggu|priok|priuk|sudirman|purwakarta|cinere|rawalumbu|kemayoran|serpong|duren sawit|jatinegara|cengkareng|bsd|kemang|pasar rebo|jakpus|matraman|cilincing|senayan|ciputat|cibitung|kebayoran|pancoran|pulogadung|tanjung duren|tangeran|kramat jati|petamburan|cibinong|koja|pondok gede|kebon jeruk|kelapa gading|tambora|pondok aren|menteng|pulo gadung"
    mask_sby = "surabaya|sby"
    mask_bdg = "bandung|bdg"
    mask_other = "banten|serang|cilegon|yogyakarta|yogya|jogja|semarang|cibubur|jawa|sidoarjo|malang|cimahi|sukabumi|cianjur|cirebon|gresik|pamulang|mojokerto|banyuwangi|kebumen|lebak bulus|garut|sleman|sragen|subang|tegal|tasikmalaya|klaten|madiun|solo|magelang|rembang|indramayu|purwokerto|pandeglang|blora|purworejo|batang|boyolali|probolinggo|karanganyar|salatiga|jepara|demak|wonosobo|banjar|cilacap|banyumas|blitar|tuban|tulungagung|jember|jombang|surakarta|solo"
    mask_outside = "sumatra|sumatera|sulawesi|medan|batam|bali|riau|pekanbaru|lampung|palembang|kalimantan|jambi|banjarmasin|samarinda|singapore|pekanbaru|palangkaraya|padang|papua|bengkulu|pontianak|makassar|makasar|manado|aceh|deli|palu|denpasar|pematangsiantar|gowa|gorontalo|malaysia|ntb|pekan baru|jayapura|maluku|ambon|korea|karimun|samosir|bone|sulsel|denppasar|bolaang|flores|ogan ilir|bangka|kupang|bukittinggi|qatar|nusa tenggara|gianyar"

    conditions = [
        (city_col.str.lower().str.contains(mask_jabo, na=False)) | (street_col.str.lower().str.contains(mask_jabo, na=False)),
        (city_col.str.lower().str.contains(mask_sby, na=False)) | (street_col.str.lower().str.contains(mask_sby, na=False)),
        (city_col.str.lower().str.contains(mask_bdg, na=False)) | (street_col.str.lower().str.contains(mask_bdg, na=False)),
        (city_col.str.lower().str.contains(mask_other, na=False)) | (street_col.str.lower().str.contains(mask_other, na=False)),
        (city_col.str.lower().str.contains(mask_outside,na=False,)) | (street_col.str.lower().str.contains(mask_outside,na=False,)),
    ]
    choices = [
        "Jabodetabek",
        "Surabaya",
        "Bandung",
        "Other Java Region",
        "Outside Java",
    ]
    return np.select(conditions, choices, default="Unidentified")