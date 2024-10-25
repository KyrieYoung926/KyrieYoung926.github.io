import json
from datetime import datetime, timedelta

# JSON 文件路径
json_file = 'mood_data.json'
# Markdown 文件路径
markdown_file = 'source/_posts/MyMood.md'

# 读取当前心情数据
def load_mood_data():
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "today": 0,
            "week_avg": 0.0,
            "last_week_avg": 0.0,
            "history": []
        }

# 保存心情数据到 JSON 文件
def save_mood_data(data):
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 更新 Markdown 文件内容
def update_markdown(data):
    # 生成嵌入的 JavaScript 代码
    js_data = f"""
<script>
// 心情数据嵌入
const moodData = {{
    "today": {data['today']},
    "week_avg": {data['week_avg']},
    "last_week_avg": {data['last_week_avg']},
    "history": {json.dumps(data['history'], ensure_ascii=False)}
}};
</script>
    """
    # 加载原有 Markdown 文件内容
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查是否已有心情数据脚本，如果有则替换；没有则插入到文件的开头
    if "<script>// 心情数据嵌入" in content:
        content = content.split("<script>// 心情数据嵌入")[0] + js_data + "\n" + "\n".join(content.split("\n")[2:])
    else:
        content = js_data + "\n" + content

    # 将更新后的内容写入 Markdown 文件
    with open(markdown_file, 'w', encoding='utf-8') as f:
        f.write(content)

# 更新心情数据并重新生成 Markdown 文件
def update_mood_data():
    data = load_mood_data()

    # 获取今天的日期和心情评分
    today_date = datetime.now()
    today_mood = int(input("请输入今天的心情评分（0-10）："))
    daily_summary = input("请输入今日心情总结：")

    # 更新 today 和 history
    today_entry = {
        "date": today_date.strftime('%Y-%m-%d'),
        "mood": today_mood,
        "summary": daily_summary
    }
    data['today'] = today_mood

    # 检查今天是否已经在历史记录中
    history_dates = [entry['date'] for entry in data['history']]
    if today_entry['date'] in history_dates:
        for entry in data['history']:
            if entry['date'] == today_entry['date']:
                entry.update(today_entry)
    else:
        data['history'].append(today_entry)

    # 更新周和上周的平均心情
    week_start = today_date - timedelta(days=today_date.weekday())
    last_week_start = week_start - timedelta(days=7)
    last_week_end = week_start - timedelta(days=1)

    data['week_avg'] = round(sum(e['mood'] for e in data['history'] if week_start.strftime('%Y-%m-%d') <= e['date']) / 7, 2)
    data['last_week_avg'] = round(sum(e['mood'] for e in data['history'] if last_week_start.strftime('%Y-%m-%d') <= e['date'] <= last_week_end.strftime('%Y-%m-%d')) / 7, 2)

    # 保存 JSON 文件和更新 Markdown
    save_mood_data(data)
    update_markdown(data)
    print("心情数据和 Markdown 文件已更新！")

if __name__ == '__main__':
    update_mood_data()
