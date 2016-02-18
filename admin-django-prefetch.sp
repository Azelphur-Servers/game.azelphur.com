/**
 * vim: set ts=4 :
 * =============================================================================
 * SourceMod SQL Admins Plugin (Prefetch)
 * Prefetches admins from an SQL database without threading.
 *
 * SourceMod (C)2004-2008 AlliedModders LLC.  All rights reserved.
 * =============================================================================
 *
 * This program is free software; you can redistribute it and/or modify it under
 * the terms of the GNU General Public License, version 3.0, as published by the
 * Free Software Foundation.
 * 
 * This program is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
 * details.
 *
 * You should have received a copy of the GNU General Public License along with
 * this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * As a special exception, AlliedModders LLC gives you permission to link the
 * code of this program (as well as its derivative works) to "Half-Life 2," the
 * "Source Engine," the "SourcePawn JIT," and any Game MODs that run on software
 * by the Valve Corporation.  You must obey the GNU General Public License in
 * all respects for all other code used.  Additionally, AlliedModders LLC grants
 * this exception to all derivative works.  AlliedModders LLC defines further
 * exceptions, found in LICENSE.txt (as of this writing, version JULY-31-2007),
 * or <http://www.sourcemod.net/license.php>.
 *
 * Version: $Id$
 */

/**
 * This file is a modified version of SourceMods original SQL Admins, it contains
 * very minimal changes, mostly just that the SQL queries have been modified
 * to run against Djangos and Python Social Auth database schema.
 */

/* We like semicolons */
#pragma semicolon 1

#include <sourcemod>
#include <csteamid>

public Plugin:myinfo = 
{
	name = "Django Admins (Prefetch)",
	author = "Azelphur",
	description = "Reads all admins from django",
	version = SOURCEMOD_VERSION,
	url = "http://www.sourcemod.net/"
};

public OnRebuildAdminCache(AdminCachePart:part)
{
	/* First try to get a database connection */
	char error[255];
	Database db;
	
	if (SQL_CheckConfig("admins"))
	{
		db = SQL_Connect("admins", true, error, sizeof(error));
	} else {
		db = SQL_Connect("default", true, error, sizeof(error));
	}
	
	if (db == null)
	{
		LogError("Could not connect to database \"default\": %s", error);
		return;
	}
	
	if (part == AdminCache_Overrides)
	{
		FetchOverrides(db);
	} else if (part == AdminCache_Groups) {
		FetchGroups(db);
	} else if (part == AdminCache_Admins) {
		FetchUsers(db);
	}
	
	delete db;
}

stock ToAccountID(String:auth[])
{
    if(strlen(auth)<11)
        return 0;
    return StringToInt(auth[10])*2 + auth[8]-48;
}

void FetchUsers(Database db)
{
	char query[255], error[255];
	DBResultSet rs;
    /*
        id == user_id
        identity == uid
        Format(query, sizeof(query), "SELECT id, authtype, identity, password, flags, name, immunity FROM sm_admins");
    */
    
	Format(query, sizeof(query), "SELECT user_id, uid FROM social_auth_usersocialauth");
	if ((rs = SQL_Query(db, query)) == null)
	{
		SQL_GetError(db, error, sizeof(error));
		LogError("FetchUsers() query failed: %s", query);
		LogError("Query error: %s", error);
		return;
	}

	char authtype[16];
	char identity[80];
	char password[80];
	char flags[32];
	char name[80];
	int immunity;
	AdminId adm;
	GroupId gid;
	int id;

	/* Keep track of a mapping from admin DB IDs to internal AdminIds to
	 * enable group lookups en masse */
	StringMap htAdmins = new StringMap();
	char key[16];
	
	while (rs.FetchRow())
	{
		id = rs.FetchInt(0);
		IntToString(id, key, sizeof(key));
		strcopy(authtype, sizeof(authtype), "steam");
		rs.FetchString(1, identity, sizeof(identity));
        CSteamIDToSteamID(identity, identity, sizeof(identity));
		strcopy(password, sizeof(password), "");
		strcopy(flags, sizeof(flags), "");
		strcopy(name, sizeof(name), "");
		immunity = 0;
		
		/* Use a pre-existing admin if we can */
		if ((adm = FindAdminByIdentity(authtype, identity)) == INVALID_ADMIN_ID)
		{
			adm = CreateAdmin(name);
			if (!BindAdminIdentity(adm, authtype, identity))
			{
				LogError("Could not bind prefetched SQL admin (authtype \"%s\") (identity \"%s\")", authtype, identity);
				continue;
			}
		}

		htAdmins.SetValue(key, adm);
		
#if defined _DEBUG
		PrintToServer("Found SQL admin (%d,%s,%s,%s,%s,%s,%d):%d", id, authtype, identity, password, flags, name, immunity, adm);
#endif
		
		/* See if this admin wants a password */
		if (password[0] != '\0')
		{
			SetAdminPassword(adm, password);
		}
		
		/* Apply each flag */
		int len = strlen(flags);
		AdminFlag flag;
		for (new i=0; i<len; i++)
		{
			if (!FindFlagByChar(flags[i], flag))
			{
				continue;
			}
			SetAdminFlag(adm, flag, true);
		}

		SetAdminImmunityLevel(adm, immunity);
	}

	delete rs;

    /* 
        Format(query, sizeof(query), "SELECT ag.admin_id AS id, g.name FROM sm_admins_groups ag JOIN sm_groups g ON ag.group_id = g.id  ORDER BY id, inherit_order ASC");
    */

	Format(query, sizeof(query), "SELECT auth_user_groups.user_id AS user_id, auth_group.name AS auth_group_name FROM auth_user_groups LEFT JOIN auth_group ON auth_user_groups.group_id = auth_group.id;");
	if ((rs = SQL_Query(db, query)) == null)
	{
		SQL_GetError(db, error, sizeof(error));
		LogError("FetchUsers() query failed: %s", query);
		LogError("Query error: %s", error);
		return;
	}

	char group[80];
	while (rs.FetchRow())
	{
		IntToString(rs.FetchInt(0), key, sizeof(key));
		rs.FetchString(1, group, sizeof(group));

		if (htAdmins.GetValue(key, adm))
		{
			if ((gid = FindAdmGroup(group)) == INVALID_GROUP_ID)
			{
				/* Group wasn't found, don't bother with it.  */
				continue;
			}

			AdminInheritGroup(adm, gid);
		}
	}
	
	delete rs;
	delete htAdmins;
}

FetchGroups(Database db)
{
}

FetchOverrides(Database db)
{
}

