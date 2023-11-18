import binascii
import os


def guess_ext(filename)->list[str]: # filename:str - 파일 경로
    enable_list = []
    
    # 파일 시그니처와 해당 확장자 매핑
    # 리스트를 리턴하는 방식으로 구현하여 시그니처가 동일한 다른 확장자에 대한 목록을 리턴
    header_signatures = {
        b'\xFF\xD8\xFF': ['jpg/jpeg'],
        b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A': ['png'],
        b'\x47\x49\x46\x38\x37\x61': ['gif'],
        b'\x47\x49\x46\x38\x39\x61': ['gif'],
        b'\x42\x4D': ['bmp'],
        b'\x49\x20\x49': ['tif'],
        b'\x49\x20\x2A\x00': ['tiff'],
        b'\x50\x4B\x03\x04': ['zip'],
        b'\x50\x4B\x05\x06': ['zip'],
        b'\x50\x4B\x07\x08': ['zip'],
        b'\x7B\x5C\x72\x74\x66': ['rtf'],
        b'\x25\x50\x44\x46': ['pdf'],
        b'\x4D\x5A': ['exe'],
        b'\x4D\x5A\x90\x00\x03\x00\x00\x00': ['exe'],
        b'\x4D\x5A\x50\x00\x02\x00\x00\x00': ['exe'],
        b'\x4D\x5A\x4E\x00\x02\x00\x00\x00': ['exe'],
        b'\x4D\x5A\x6E\x00\x00\x00\x00\x00': ['exe'],
        b'\x25\x21\x50\x53\x2D\x41\x64\x6F': ['ps'],
        b'\x25\x21\x50\x45\x0D\x0A': ['eps'],
        b'\x1F\x8B\x08': ['gz'],
        b'\x42\x5A\x68': ['bz2'],
        b'\x50\x4B\x03\x04': ['zip'],
        b'\x50\x4B\x05\x06': ['zip'],
        b'\x50\x4B\x07\x08': ['zip'],
        b'\x1F\x9D': ['jar'],
        b'\x4D\x5A\x49\x53': ['cab'],
        b'\x4D\x44\x4D\x50': ['msi'],
        b'\x43\x30\x30\x31': ['iso'],
        b'\x21\x3C\x61\x72\x63\x68\x3E': ['arc'],
        b'\x1A\x45\xDF\xA3': ['mkv'],
        b'\x1F\x43\x4F\x4D': ['z'],
        b'\x75\x73\x74\x61\x72': ['tar'],
        b'\x4C\x5A\x49\x50': ['lz'],
        b'\x28\x54\x68\x69\x73\x20\x66\x69\x6C\x65': ['hqx'],
        # 다른 파일 형식의 헤더 시그니처를 여기에 추가할 수 있습니다.
    }
    footer_signature = {
        b'\xFF\xD9': ['jpg/jpeg'],
        b'\x00\x3B': ['gif'],
        b'\x49\x45\x4E\x44\xAE\x42\x60\x82': ['png'],
        b'\x25\x25\x45\x4F\x46': ['pdf'],
        b'\x50\x4B\x05\x06': ['zip'],
        # 다른 파일 형식의 푸터 시그니처를 여기에 추가할 수 있습니다.
    }

    try:
        sign_search_len = 30
        pin = 0
        f = open(filename, "rb")

        # file size
        filelen_byte = os.path.getsize(filename)

        # pin과 연결되었을 경우 사용해야할 코드
        '''
        if has_pin(filename):
            remove_pin(filename)
            pin = 1
        '''
        
        # file size 가 작은 경우를 고려
        if filelen_byte < sign_search_len:
            sign_search_len = filelen_byte
        
        # 파일 초반 바이트를 읽어들여 파일 헤더 시그니처 목록에 매핑하여 가능한 파일 확장자 분류 
        for i in range(1, sign_search_len):
            file_signature = f.read(i)
            enable_value = header_signatures.get(file_signature)
            if enable_value:
                enable_list.extend(enable_value)
            f.seek(0)
        # 파일 후반 바이트를 읽어들여 파일 푸터 시그니처 목록에 매핑하여 가능한 파일 확장자 분류 (작성 필요)
        for i in range(1, sign_search_len):
            f.seek(filelen_byte - i)
            file_signature = f.read(i)
            enable_value = footer_signature.get(file_signature)
            if enable_value:
                enable_list.extend(enable_value)
            f.seek(0)
        f.close()
        
        # pin과 연결되었을 경우 사용해야할 코드
        '''
        if pin == 1:
            add_pin(filename)
        '''

    except FileNotFoundError: 
        print(f'Error: {filename}을(를) 찾을 수 없습니다.')
    except Exception as e:
        print(f'Error: {e}')
    
    return enable_list # list[str] - 가능한 확장자명을 리스트에 담아 출력


if __name__ == "__main__":
    # 테스팅 코드
    fd = "C:/Users/clost/Downloads/PALOMA.pdf"
    flist = guess_ext(fd)
    print(flist)
