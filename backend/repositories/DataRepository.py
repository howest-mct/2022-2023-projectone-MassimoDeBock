from .Database import Database


class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.method != 'GET' and request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    @staticmethod
    def read_status_lampen():
        sql = "SELECT * from `demo_homecontrol`.lampen"
        return Database.get_rows(sql)

    @staticmethod
    def read_status_lamp_by_id(id):
        sql = "SELECT * from demo_homecontrol.lampen WHERE id = %s"
        params = [id]
        return Database.get_one_row(sql, params)

    @staticmethod
    def update_status_lamp(id, status):
        sql = "UPDATE demo_homecontrol.lampen SET status = %s WHERE id = %s"
        params = [status, id]
        return Database.execute_sql(sql, params)

    @staticmethod
    def update_status_alle_lampen(status):
        sql = "UPDATE demo_homecontrol.lampen SET status = %s"
        params = [status]
        return Database.execute_sql(sql, params)

    @staticmethod
    def GetNextScheduledMedication():
        sql = "SELECT * FROM DocterPablo.MedicationIntake MI where MI.Status != \"Taken\" order by Time limit 1"
        return Database.get_one_row(sql)

    @staticmethod
    def LoginUser(username, password):
        sql = "SELECT * FROM DocterPablo.SettingsProfile SP where SP.Name = %s and SP.Password = %s limit 1"
        params = [username, password]
        row = Database.get_one_row(sql, params)
        if row == None:
            return None
        else:
            return row["Settings"]

    @staticmethod
    def LoginAny(username):
        sql = "SELECT * FROM DocterPablo.SettingsProfile SP where SP.Password = %s limit 1"
        params = [username]
        row = Database.get_one_row(sql, params)
        if row == None:
            return None
        else:
            return row["Settings"]

    @staticmethod
    def LogComponents(component, value):
        sql = "insert into DocterPablo.ComponentValue values (NOW(), %s, %s)"
        params = [component, value]
        result = Database.execute_sql(sql, params)
        if result == None:
            print("something went wrong with logging a component")
        return

    @staticmethod
    def GetDispenserInfo():
        sql = "         SELECT U.Name AS FirstName, U.LastName, DATE_FORMAT(MI.Time, '%Y-%m-%d %H:%i:%s') AS Time, MI.Patient, MI.TypeId, MI.Status, MI.Delay, MI.RelatedDoctorId, MI.Dosage, MT.* FROM DocterPablo.UserInfo U JOIN (     SELECT *     FROM (         SELECT *         FROM DocterPablo.MedicationIntake MI         WHERE MI.Status = 'Taken'         ORDER BY MI.Time DESC         LIMIT 2     ) AS Subquery1     UNION ALL     SELECT *     FROM (         SELECT *         FROM DocterPablo.MedicationIntake MI         WHERE MI.Status != 'Taken'         ORDER BY MI.Time         LIMIT 3     ) AS Subquery2 ) AS MI ON MI.Patient = U.Id JOIN DocterPablo.MedicationType MT ON MI.TypeId = MT.Id"
        result = Database.get_rows(sql)
        return result

    @staticmethod
    def InsertUser(Name, LastName, PhoneNumber, PhoneNumberResponsible, RFID):
        sql = "insert into DocterPablo.UserInfo (Name, LastName, PhoneNumber, PhoneNumberResponsible, RFID) values (%s, %s,%s,%s,%s)"
        params = [Name, LastName, PhoneNumber, PhoneNumberResponsible, RFID]
        result = Database.execute_sql(sql, params)
        if result == None:
            print("invalid user wth")
        return

    @staticmethod
    def SetNextDropActive():
        sql = "UPDATE DocterPablo.MedicationIntake SET Status = 'InProgress' WHERE MedicationIntake.Status != 'Taken' ORDER BY MedicationIntake.Time LIMIT 1"
        result = Database.execute_sql(sql)
        if result == None:
            print("invalid dropactive somehow..")
        print(f"{result} changes")
        return

    @staticmethod
    def SetActiveDropTaken():
        sql = "UPDATE DocterPablo.MedicationIntake SET Status = 'Taken' WHERE MedicationIntake.Status = 'InProgress' ORDER BY MedicationIntake.Time LIMIT 1;"
        result = Database.execute_sql(sql)
        if result == None:
            print("invalid droptaken somehow..")
        return
