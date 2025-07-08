from datetime import datetime
import pytz


def convert_dates_to_kst(doc: dict, keys: list) -> dict:
    """
    주어진 dict에서 keys 리스트에 해당하는 datetime string을
    한국시간으로 변환 후 'YYYY-MM-DD HH:MM:SS' 포맷으로 변경한다.
    """
    kst = pytz.timezone("Asia/Seoul")

    for key in keys:
        dt_str = doc.get(key)
        if dt_str:
            try:
                # 1. 문자열 → datetime 파싱
                dt_utc = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S.%fZ")
                dt_utc = dt_utc.replace(tzinfo=pytz.UTC)

                # 2. UTC → KST 변환
                dt_kst = dt_utc.astimezone(kst)

                # 3. 포맷팅
                doc[key] = dt_kst.strftime("%Y-%m-%d %H:%M:%S")
            except Exception as e:
                print(f"Error converting {key}: {e}")
    return doc
