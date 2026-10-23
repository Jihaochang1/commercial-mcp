#!/usr/bin/env python3
"""Script to publish technical blog posts to multiple platforms."""

import json
import subprocess
import sys
from pathlib import Path

PLATFORMS = {
    "juejin": {
        "name": "掘金",
        "url": "https://juejin.cn",
        "status": "manual",  # Need manual login
        "note": "请使用掘金API或手动发布"
    },
    "medium": {
        "name": "Medium", 
        "url": "https://medium.com",
        "status": "api",
        "note": "需要Medium API token"
    },
    "devto": {
        "name": "Dev.to",
        "url": "https://dev.to",
        "status": "manual",
        "note": "可以使用devto gem或手动发布"
    },
    "csdn": {
        "name": "CSDN",
        "url": "https://blog.csdn.net",
        "status": "manual",
        "note": "手动发布到博客"
    }
}

def check_platform_status():
    """Check which platforms are available."""
    print("=" * 60)
    print("博客发布平台检查")
    print("=" * 60)
    
    for platform, config in PLATFORMS.items():
        status_icon = "✅" if config["status"] == "manual" else "⚠️"
        print(f"\n{status_icon} {config['name']} ({platform})")
        print(f"   URL: {config['url']}")
        print(f"   状态: {config['status']}")
        print(f"   说明: {config['note']}")
    
    print("\n" + "=" * 60)

def create_blog_post(title: str, content: str, tags: list[str]) -> dict:
    """Create a blog post dict for multiple platforms."""
    return {
        "title": title,
        "content": content,
        "tags": tags,
        "platforms": list(PLATFORMS.keys()),
        "published_at": None
    }

def save_post(post: dict, output_dir: Path):
    """Save blog post as JSON."""
    output_file = output_dir / f"{post['title'][:20]}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(post, f, ensure_ascii=False, indent=2)
    print(f"已保存: {output_file}")
    return output_file

def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="博客发布工具")
    parser.add_argument("--check", action="store_true", help="检查平台状态")
    parser.add_argument("--create", type=str, help="创建博客草稿")
    parser.add_argument("--title", type=str, help="博客标题")
    parser.add_argument("--tags", nargs="*", help="标签列表")
    
    args = parser.parse_args()
    
    if args.check:
        check_platform_status()
    elif args.create:
        # Read content from file or stdin
        content_file = Path(args.create)
        if content_file.exists():
            content = content_file.read_text(encoding='utf-8')
        else:
            print(f"文件不存在: {content_file}")
            sys.exit(1)
        
        tags = args.tags or ["MCP", "Python", "开源", "变现"]
        post = create_blog_post(args.title or "未命名博客", content, tags)
        
        output_dir = Path(__file__).parent / "drafts"
        output_dir.mkdir(exist_ok=True)
        save_post(post, output_dir)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
