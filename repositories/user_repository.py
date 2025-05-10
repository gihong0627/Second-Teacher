from firebase_admin import firestore

class UserRepository:
    def __init__(self):
        self.db = firestore.client()
        self.collection = self.db.collection('users')
    
    def exists(self, user_id):
        """사용자 문서 존재 여부 확인"""
        doc = self.collection.document(user_id).get()
        return doc.exists
    
    def create(self, user_id, email):
        """새 사용자 문서 생성"""
        user_data = {
            'email': email,
            'createdAt': firestore.SERVER_TIMESTAMP
        }
        self.collection.document(user_id).set(user_data)
    
    def pdf_exists(self, user_id):
        """pdf/UID 컬렉션에 사용자 uid 문서 존재 여부 확인"""
        # 먼저 UID 문서가 있는지 확인
        uid_ref = self.db.collection('pdf').document('UID')
        uid_doc = uid_ref.get()
        
        if not uid_doc.exists:
            # UID 문서가 없으면 생성
            uid_ref.set({})
            return False
        
        # 사용자 문서 존재 여부 확인 - 문서가 있는지 직접 확인
        user_pdf_ref = self.db.collection('pdf').document('UID').collection(user_id).document(user_id)
        user_pdf_doc = user_pdf_ref.get()
        
        return user_pdf_doc.exists
    
    def create_pdf_document(self, user_id):
        """pdf/UID 컬렉션에 사용자 uid 이름의 빈 문서 생성"""
        user_pdf_ref = self.db.collection('pdf').document('UID').collection(user_id).document(user_id)
        user_pdf_ref.set({})
        print(f"Created empty document at pdf/UID/{user_id}/{user_id}")