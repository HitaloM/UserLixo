import math
import os
import time

from PIL import Image
from db import db, save
from pyrogram import Client, Filters
from pyrogram.errors import StickersetInvalid
from pyrogram.api import functions, types


@Client.on_message(Filters.command("kibe", prefixes='.') & Filters.me)
def kibe(client, message):
    emoji = message.text[6:]
    rsize = False
    ctime = time.time()
    user = client.get_me()
    if not user.username:
        user.username = user.first_name
    if 'sticker' in db:
        pack = db['sticker']
    else:
        pack = 1
    packname = f"a{user.id}_by_{user.username}_{pack}"
    packnick = f"@{user.username}'s kibe pack V{pack}.0"
    rmessage = message.reply_to_message
    if rmessage and rmessage.media:
        if rmessage.photo:
            photo = client.download_media(rmessage.photo.file_id, rmessage.photo.file_ref, file_name=f'./{ctime}.png')
            rsize = True
        elif rmessage.document:
            photo = client.download_media(rmessage.document.file_id, rmessage.document.file_ref,
                                          file_name=f'./{ctime}.png')
            rsize = True
        elif rmessage.sticker:
            if len(emoji) == 0:
                emoji = rmessage.sticker.emoji
            if rmessage.sticker.is_animated:
                photo = client.download_media(rmessage.sticker.file_id, rmessage.sticker.file_ref,
                                              file_name=f'./{ctime}.tgs')
                packname += '_animated'
                packnick += ' animated'
            else:
                photo = client.download_media(rmessage.sticker.file_id, rmessage.sticker.file_ref,
                                              file_name=f'./{ctime}.webp')
                rsize = True
        if not emoji:
            emoji = "👍"
        if rsize:
            photo = resize_photo(photo, ctime)
        try:
            stickerpack = client.send(functions.messages.GetStickerSet(stickerset=types.InputStickerSetShortName(short_name=packname)))
        except StickersetInvalid:
            pack_exists = False
        else:
            pack_exists = True
        st = 'Stickers'
        if not pack_exists:
            create_pack(message, client, st, packnick, photo, emoji, packname)
        elif stickerpack.set.count > 119:
            pack += 1
            db['sticker'] = pack
            save(db)
            packname = f"a{user.id}_by_{user.username}_{pack}"
            create_pack(message, client, st, packnick, photo, emoji, packname)
        else:
            # Add a new sticker
            client.send_message(st, '/addsticker')
            # Define pack name
            client.send_message(st, packname)
            # Send sticker image
            client.send_document(st, photo)
            # Send sticker emoji
            client.send_message(st, emoji)
            time.sleep(0.3)
            # We are done
            client.send_message(st, '/done')
            message.edit(f'[kibed](http://t.me/addstickers/{packname})')
            os.remove(photo)


def resize_photo(photo, ctime):
    """ Resize the given photo to 512x512 """
    image = Image.open(photo)
    maxsize = (512, 512)
    if (image.width and image.height) < 512:
        size1 = image.width
        size2 = image.height
        if image.width > image.height:
            scale = 512 / size1
            size1new = 512
            size2new = size2 * scale
        else:
            scale = 512 / size2
            size1new = size1 * scale
            size2new = 512
        size1new = math.floor(size1new)
        size2new = math.floor(size2new)
        sizenew = (size1new, size2new)
        image = image.resize(sizenew)
    else:
        image.thumbnail(maxsize)
    os.remove(photo)
    image.save(f'./{ctime}.png')

    return f'./{ctime}.png'


def create_pack(message, client, st, packnick, photo, emoji, packname):
    message.edit('criando novo pack')
    # Create pack
    client.send_message(st, '/newpack')
    # Set a name for it
    client.send_message(st, packnick)
    # Send the first sticker of the pack
    client.send_document(st, photo)
    # Send the emoji for the first sticker
    client.send_message(st, emoji)
    time.sleep(0.3)
    # Publish the sticker pack
    client.send_message(st, '/publish')
    # Skip setting sticker pack icon
    client.send_message(st, '/skip')
    # Set sticker pack url
    client.send_message(st, packname)
    message.edit(f'[kibed](http://t.me/addstickers/{packname})')
    os.remove(photo)
