#!/usr/bin/env python3
"""License Key Manager for FoodCalorie MCP Server Pro tier."""

import sqlite3
import hashlib
import uuid
from datetime import datetime, timedelta
from typing import Optional
from pathlib import Path


class LicenseManager:
    """Simple license key management system."""
    
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or str(Path(__file__).parent / "licenses.db")
        self.conn = sqlite3.connect(self.db_path)
        self._create_tables()
    
    def _create_tables(self):
        """Create licenses table."""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS licenses (
                key TEXT PRIMARY KEY,
                user_email TEXT NOT NULL,
                tier TEXT DEFAULT 'free',
                expires_at TIMESTAMP,
                max_uses INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_used_at TIMESTAMP
            )
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS usage_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                license_key TEXT,
                action TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (license_key) REFERENCES licenses(key)
            )
        """)
        self.conn.commit()
    
    def generate_key(self, tier: str = "pro", days: int = 30) -> str:
        """Generate a new license key."""
        key = f"FC-{uuid.uuid4().hex[:12].upper()}"
        expires_at = datetime.now() + timedelta(days=days)
        
        self.conn.execute(
            """INSERT OR REPLACE INTO licenses 
               (key, user_email, tier, expires_at) 
               VALUES (?, ?, ?, ?)""",
            (key, "pending", tier, expires_at)
        )
        self.conn.commit()
        return key
    
    def activate(self, key: str, user_email: str) -> dict:
        """Activate a license key."""
        cursor = self.conn.execute(
            "SELECT * FROM licenses WHERE key = ?", (key,)
        )
        license = cursor.fetchone()
        
        if not license:
            return {"success": False, "error": "Invalid license key"}
        
        if license[4] and datetime.now() > datetime.fromisoformat(license[4]):
            return {"success": False, "error": "License expired"}
        
        self.conn.execute(
            """UPDATE licenses 
               SET user_email = ?, last_used_at = CURRENT_TIMESTAMP 
               WHERE key = ?""",
            (user_email, key)
        )
        self.conn.commit()
        
        return {
            "success": True,
            "tier": license[2],
            "expires_at": license[3]
        }
    
    def verify(self, key: str) -> dict:
        """Verify if a license key is valid."""
        cursor = self.conn.execute(
            """SELECT key, tier, expires_at, max_uses, last_used_at 
               FROM licenses WHERE key = ?""",
            (key,)
        )
        license = cursor.fetchone()
        
        if not license:
            return {"valid": False, "reason": "Key not found"}
        
        if license[2] and datetime.now() > datetime.fromisoformat(license[2]):
            return {"valid": False, "reason": "Expired"}
        
        if license[3] and license[3] > 0:
            # Check usage limit
            pass
        
        # Log usage
        self.conn.execute(
            """INSERT INTO usage_logs (license_key, action) 
               VALUES (?, 'verify')""",
            (key,)
        )
        self.conn.commit()
        
        return {
            "valid": True,
            "tier": license[1],
            "expires_at": license[2],
            "remaining_uses": license[3] if license[3] else "unlimited"
        }
    
    def get_stats(self) -> dict:
        """Get license statistics."""
        cursor = self.conn.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN tier = 'pro' THEN 1 ELSE 0 END) as pro_count,
                SUM(CASE WHEN tier = 'enterprise' THEN 1 ELSE 0 END) as enterprise_count,
                SUM(CASE WHEN expires_at IS NOT NULL AND expires_at > datetime('now') THEN 1 ELSE 0 END) as active_count
            FROM licenses
        """)
        row = cursor.fetchone()
        
        return {
            "total_licenses": row[0],
            "pro_users": row[1],
            "enterprise_users": row[2],
            "active_licenses": row[3]
        }
    
    def close(self):
        """Close database connection."""
        self.conn.close()


def main():
    """CLI interface for license management."""
    import argparse
    
    parser = argparse.ArgumentParser(description="FoodCalorie License Manager")
    parser.add_argument("action", choices=["generate", "activate", "verify", "stats"])
    parser.add_argument("--key", help="License key")
    parser.add_argument("--email", help="User email")
    parser.add_argument("--tier", default="pro", choices=["pro", "enterprise"])
    parser.add_argument("--days", type=int, default=30, help="License duration in days")
    
    args = parser.parse_args()
    
    lm = LicenseManager()
    
    if args.action == "generate":
        key = lm.generate_key(tier=args.tier, days=args.days)
        print(f"Generated license key: {key}")
        print(f"Tier: {args.tier}")
        print(f"Expires in: {args.days} days")
    
    elif args.action == "activate":
        if not args.key or not args.email:
            print("Error: --key and --email required")
            return
        result = lm.activate(args.key, args.email)
        print(result)
    
    elif args.action == "verify":
        if not args.key:
            print("Error: --key required")
            return
        result = lm.verify(args.key)
        print(result)
    
    elif args.action == "stats":
        stats = lm.get_stats()
        print(f"Total licenses: {stats['total_licenses']}")
        print(f"Pro users: {stats['pro_users']}")
        print(f"Enterprise users: {stats['enterprise_users']}")
        print(f"Active licenses: {stats['active_licenses']}")
    
    lm.close()


if __name__ == "__main__":
    main()
