# Sayfalama callback handler'ı ekleyin bot.py'deki button_callback metoduna

# Bu kodu button_callback metoduna ekleyin:
        elif query.data.startswith("matches_page_"):
            # Sayfa numarasını al
            page_num = int(query.data.split("_")[-1])
            await self.today_matches(update, context, page=page_num)
