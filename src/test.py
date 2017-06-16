from model import User

def main():
    u = User(username='seb', password='somepass')
    u.save()


if __name__ == '__main__':
    main()
