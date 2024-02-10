
// Example of a enum in C which has different syntax and different support in Sphinx to the C++ enum

/**
 * Backup data.
 *
 * \ingroup Backup
 */
typedef enum {
	/**
	 * Compatibility with old gboolean used instead of format.
	 *
	 * File type is guessed for extension, non unicode format used
	 * for Gammu backup.
	 */
	GSM_Backup_Auto = 0,
	/**
	 * Compatibility with old gboolean used instead of format.
	 *
	 * File type is guessed for extension, unicode format used
	 * for Gammu backup.
	 */
	GSM_Backup_AutoUnicode = 1,
	/**
	 * LMB format, compatible with Logo manager, can store
	 * phonebooks and logos.
	 */
	GSM_Backup_LMB,
	/**
	 * vCalendar standard, can store todo and calendar entries.
	 */
	GSM_Backup_VCalendar,
	/**
	 * vCard standard, can store phone phonebook entries.
	 */
	GSM_Backup_VCard,
	/**
	 * LDIF (LDAP Data Interchange Format), can store phone
	 * phonebook entries.
	 */
	GSM_Backup_LDIF,
	/**
	 * iCalendar standard, can store todo and calendar entries.
	 */
	GSM_Backup_ICS,
	/**
	 * Gammu own format can store almost anything from phone.
	 *
	 * This is ASCII version of the format, Unicode strings are HEX
	 * encoded. Use GSM_Backup_GammuUCS2 instead if possible.
	 */
	GSM_Backup_Gammu,
	/**
	 * Gammu own format can store almost anything from phone.
	 *
	 * This is UCS2-BE version of the format.
	 */
	GSM_Backup_GammuUCS2,
	/**
	 * vNote standard, can store phone notes.
	 */
	GSM_Backup_VNote,
} GSM_BackupFormat;
