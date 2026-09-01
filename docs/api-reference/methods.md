# جدول مرجع متدهای API (API Methods Reference)

جدول تمامی متدهای پیاده‌سازی شده در کلاس `Bot`:

| نام متد در کتابخانه | اندپوینت در سروش‌پلاس | خروجی بازگشتی | توضیحات |
|---|---|---|---|
| `get_me()` | `/getMe` | `User` | دریافت اطلاعات خود بات |
| `send_message()` | `/sendMessage` | `Message` | ارسال پیام متنی با پشتیبانی از کیبوردها و فرمت HTML/Markdown |
| `forward_message()` | `/forwardMessage` | `Message` | فوروارد پیام از چتی به چت دیگر |
| `copy_message()` | `/copyMessage` | `MessageId` | کپی پیام بدون نام فرستنده اصلی |
| `send_photo()` | `/sendPhoto` | `Message` | ارسال عکس (URL یا فایل محلی InputFile) |
| `send_audio()` | `/sendAudio` | `Message` | ارسال فایل صوتی |
| `send_document()` | `/sendDocument` | `Message` | ارسال اسناد و فایل‌های متفرقه |
| `send_video()` | `/sendVideo` | `Message` | ارسال فایل ویدیویی |
| `send_animation()` | `/sendAnimation` | `Message` | ارسال انیمیشن (GIF / MP4) |
| `send_voice()` | `/sendVoice` | `Message` | ارسال پیام صوتی (Voice) |
| `send_video_note()` | `/sendVideoNote` | `Message` | ارسال پیام ویدیویی دایره‌ای |
| `send_media_group()` | `/sendMediaGroup` | `list[Message]` | ارسال آلبوم چندرسانه‌ای |
| `send_location()` | `/sendLocation` | `Message` | ارسال مختصات جغرافیایی |
| `send_contact()` | `/sendContact` | `Message` | ارسال کارت تماس مخاطب |
| `send_sticker()` | `/sendSticker` | `Message` | ارسال استیکر |
| `send_chat_action()` | `/sendChatAction` | `bool` | نمایش وضعیت در حال تایپ / آپلود |
| `get_file()` | `/getFile` | `File` | دریافت متادیتای مسیر فایل |
| `download_file()` | `/file/bot<token>/...` | `Path / BinaryIO` | دانلود استریم فایل روی دیسک یا بافر |
| `edit_message_text()` | `/editMessageText` | `Message / bool` | ویرایش متن پیام قبلی |
| `edit_message_caption()` | `/editMessageCaption` | `Message / bool` | ویرایش کپشن رسانه قبلی |
| `edit_message_media()` | `/editMessageMedia` | `Message / bool` | تعویض رسانه پیام قبلی |
| `edit_message_reply_markup()` | `/editMessageReplyMarkup` | `Message / bool` | ویرایش کیبورد پیام قبلی |
| `delete_message()` | `/deleteMessage` | `bool` | حذف یک پیام در چت |
| `answer_callback_query()` | `/answerCallbackQuery` | `bool` | پاسخ به رویداد کلیک دکمه اینلاین و نمایش پاپ‌آپ |
| `set_my_commands()` | `/setMyCommands` | `bool` | تنظیم لیست دستورات منوی ربات |
| `get_my_commands()` | `/getMyCommands` | `list[BotCommand]` | دریافت لیست دستورات ثبت‌شده |
| `delete_my_commands()` | `/deleteMyCommands` | `bool` | حذف لیست دستورات |
| `pin_chat_message()` | `/pinChatMessage` | `bool` | پین کردن پیام در چت |
| `unpin_chat_message()` | `/unpinChatMessage` | `bool` | آن‌پین کردن پیام در چت |
| `get_chat()` | `/getChat` | `Chat` | دریافت اطلاعات کامل یک چت یا کانال |
| `get_user_profile_photos()` | `/getUserProfilePhotos` | `UserProfilePhotos` | دریافت تصاویر پروفایل کاربر |
| `get_sticker_set()` | `/getStickerSet` | `StickerSet` | دریافت پک استیکر |
| `get_updates()` | `/getUpdates` | `list[Update]` | دریافت به‌روزرسانی‌ها در حالت Polling |
| `set_webhook()` | `/setWebhook` | `bool` | تنظیم آدرس URL وبهوک |
| `delete_webhook()` | `/deleteWebhook` | `bool` | حذف وبهوک و بازگشت به Polling |
| `get_webhook_info()` | `/getWebhookInfo` | `WebhookInfo` | بررسی وضعیت وبهوک فعلی |
