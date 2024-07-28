# -*- coding: utf-8 -*-

import os
from rich.console import Console
from unit3dup.command import cli
from unit3dup.files import Files
from unit3dup.automode import Auto
from unit3dup.uploader import UploadBot
from unit3dup.search import TvShow
from unit3dup.torrent import Torrent
from unit3dup.pvtVideo import Video
from unit3dup.qbitt import Qbitt
from unit3dup.pvtTorrent import Mytorrent

console = Console(log_path=False)


def main():
    """ Auto Mode """
    if cli.args.scan:
        # New instance with cli.path
        auto = Auto(cli.args.scan)

        # Walk through the path
        series, movies = auto.scan()

        # For each item
        for item in series + movies:
            """
            Getting ready for tracker upload
            Return
                  - torrent name (filename or folder name)
                  - tracker name ( TODO: load config at start)
                  - content category ( movie or serie)
                  - torrent meta_info 
            """

            video_files = Files(path=item.torrent_path,
                                tracker=cli.args.tracker,
                                media_type=item.media_type,
                                torrent_name=item.torrent_name
                                )
            content = video_files.get_data()
            if content is False:
                # skip invalid folder or file
                continue

            """ Request results from the TVshow online database """
            my_tmdb = TvShow(content.category)
            tv_show_result = my_tmdb.start(content.file_name)

            """ Return info about HD or Standard , MediaInfo, Description (screenshots), Size value for free_lech """
            video_info = Video(
                fileName=str(os.path.join(content.folder, content.file_name))
            )

            """ Hashing """
            my_torrent = Mytorrent(contents=content, meta=content.metainfo)
            my_torrent.write()

            """ the bot is getting ready to send the payload """
            unit3d_up = UploadBot(content)

            """ Send """
            tracker_response = unit3d_up.send(tv_show=tv_show_result, video=video_info)

            """ Qbittorrent """
            Qbitt(tracker_data_response=tracker_response, torrent=my_torrent, contents=content)

    """ COMMANDS LIST: commands not necessary for the upload but may be useful """

    torrent_info = Torrent(cli.args.tracker)

    if cli.args.search:
        torrent_info.search(cli.args.search)
        return

    if cli.args.info:
        torrent_info.search(cli.args.info, info=True)
        return

    if cli.args.description:
        torrent_info.get_by_description(cli.args.description)
        return

    if cli.args.bdinfo:
        torrent_info.get_by_bdinfo(cli.args.bdinfo)
        return

    if cli.args.uploader:
        torrent_info.get_by_uploader(cli.args.uploader)
        return

    if cli.args.startyear:
        torrent_info.get_by_start_year(cli.args.startyear)
        return

    if cli.args.endyear:
        torrent_info.get_by_end_year(cli.args.endyear)
        return

    if cli.args.type:
        torrent_info.get_by_types(cli.args.type)
        return

    if cli.args.resolution:
        torrent_info.get_by_res(cli.args.resolution)
        return

    if cli.args.filename:
        torrent_info.get_by_filename(cli.args.filename)
        return

    if cli.args.tmdb_id:
        torrent_info.get_by_tmdb_id(cli.args.tmdb_id)
        return

    if cli.args.imdb_id:
        torrent_info.get_by_imdb_id(cli.args.imdb_id)
        return

    if cli.args.tvdb_id:
        torrent_info.get_by_tvdb_id(cli.args.tvdb_id)
        return

    if cli.args.mal_id:
        torrent_info.get_by_mal_id(cli.args.mal_id)
        return

    if cli.args.playlist_id:
        torrent_info.get_by_playlist_id(cli.args.playlist_id)
        return

    if cli.args.collection_id:
        torrent_info.get_by_collection_id(cli.args.collection_id)
        return

    if cli.args.freelech:
        torrent_info.get_by_freeleech(cli.args.freelech)
        return

    if cli.args.season:
        torrent_info.get_by_season(cli.args.season)
        return

    if cli.args.episode:
        torrent_info.get_by_episode(cli.args.episode)
        return

    if cli.args.mediainfo:
        torrent_info.get_by_mediainfo(cli.args.mediainfo)
        return

    if cli.args.alive:
        torrent_info.get_alive()
        return

    if cli.args.dead:
        torrent_info.get_dead()
        return

    if cli.args.dying:
        torrent_info.get_dying()
        return

    if cli.args.doubleup:
        torrent_info.get_doubleup()
        return

    if cli.args.featured:
        torrent_info.get_featured()
        return

    if cli.args.refundable:
        torrent_info.get_refundable()
        return

    if cli.args.stream:
        torrent_info.get_stream()
        return

    if cli.args.standard:
        torrent_info.get_sd()
        return

    if cli.args.highspeed:
        torrent_info.get_highspeed()
        return

    if cli.args.internal:
        torrent_info.get_internal()
        return

    if cli.args.personal:
        torrent_info.get_personal()
        return

    if not cli.args:
        console.print("Syntax error! Please check your commands")
        return


if __name__ == "__main__":
    main()
    print()
