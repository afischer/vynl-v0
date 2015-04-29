import gmusicapi as gm
import pickle
import getpass
email = raw_input("Email: ")
passw = getpass.getpass("Password: ")
mb = gm.clients.Mobileclient(debug_logging=True, validate=True, verify_ssl=True)
if not mb.login(email,passw):
	print "Something's wrong..."
passw=''
print mb.get_all_songs(incremental=False, include_deleted=False)
