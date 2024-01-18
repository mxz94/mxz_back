import asyncio

from bilix import DownloaderBilibili


async def main():
    async with DownloaderBilibili(videos_dir = "") as d:
        await d.get_video('https://www.bilibili.com/video/BV1pV411R7hM/?spm_id_from=333.1007.tianma.1-1-1.click')


asyncio.run(main())