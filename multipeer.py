import ui, sound, ctypes, re, json, heapq, base64, os, threading, time, sys, platform
from objc_util import *

MPVolumeView = ObjCClass('MPVolumeView')
Control = [MPVolumeView.new().autorelease().subviews()]
listFiles = []
listDirs = []
mDirName = []
MusicPath = ['']
MusicParent = ['']
RepeatDetect = ['0']
StopResending = ['0']
ReceiveM = [b'']
MusicData = [b'']
PlayDetect =['0']
LoopBreak = [False]
RepeatThread = []
seekbarThreadList = []
NowClosed = ['0']
CheckSync = ['0']

UIs = base64.b64decode("WwogIHsKICAgICJub2RlcyIgOiBbCiAgICAgIHsKICAgICAgICAibm9kZXMiIDogWwoKICAgICAgICBdLAogICAgICAgICJmcmFtZSIgOiAie3s2LCA5OH0sIHszNTMsIDE5OX19IiwKICAgICAgICAiY2xhc3MiIDogIlRhYmxlVmlldyIsCiAgICAgICAgImF0dHJpYnV0ZXMiIDogewogICAgICAgICAgInV1aWQiIDogIjk5ODk3RDJDLTYwOTMtNEU4Qy1CQkE4LTQ5MzFFNDAxQTZGRiIsCiAgICAgICAgICAiZGF0YV9zb3VyY2VfYWN0aW9uIiA6ICJTZWxlY3RGaWxlIiwKICAgICAgICAgICJiYWNrZ3JvdW5kX2NvbG9yIiA6ICJSR0JBKDAuMTI5MzA4LDAuMTI5MzA4LDAuMTI5MzA4LDEuMDAwMDAwKSIsCiAgICAgICAgICAiZnJhbWUiIDogInt7ODMsIDE4M30sIHsyMDAsIDIwMH19IiwKICAgICAgICAgICJkYXRhX3NvdXJjZV9pdGVtcyIgOiAiIiwKICAgICAgICAgICJ0aW50X2NvbG9yIiA6ICJSR0JBKDEuMDAwMDAwLDAuMDMxMjUwLDAuMDMxMjUwLDEuMDAwMDAwKSIsCiAgICAgICAgICAiZGF0YV9zb3VyY2VfbnVtYmVyX29mX2xpbmVzIiA6IDEsCiAgICAgICAgICAiZGF0YV9zb3VyY2VfZGVsZXRlX2VuYWJsZWQiIDogZmFsc2UsCiAgICAgICAgICAiZGF0YV9zb3VyY2VfZm9udF9zaXplIiA6IDE4LAogICAgICAgICAgInJvd19oZWlnaHQiIDogNDQsCiAgICAgICAgICAiY2xhc3MiIDogIlRhYmxlVmlldyIsCiAgICAgICAgICAibmFtZSIgOiAiTXVzaWNMaXN0IiwKICAgICAgICAgICJmbGV4IiA6ICJXSExSVEIiCiAgICAgICAgfSwKICAgICAgICAic2VsZWN0ZWQiIDogZmFsc2UKICAgICAgfSwKICAgICAgewogICAgICAgICJub2RlcyIgOiBbCgogICAgICAgIF0sCiAgICAgICAgImZyYW1lIiA6ICJ7ezYsIDM0N30sIHszNTMsIDQ3fX0iLAogICAgICAgICJjbGFzcyIgOiAiVGV4dFZpZXciLAogICAgICAgICJhdHRyaWJ1dGVzIiA6IHsKICAgICAgICAgICJ1dWlkIiA6ICI5NUIwMzRGNS0yMDkyLTQwRUEtODI1OS0zRTI1NUYzODgzMjYiLAogICAgICAgICAgImZvbnRfc2l6ZSIgOiAxNywKICAgICAgICAgICJjb3JuZXJfcmFkaXVzIiA6IDEsCiAgICAgICAgICAiYmFja2dyb3VuZF9jb2xvciIgOiAiUkdCQSgwLjA4NjA2OCwwLjA4NjA2OCwwLjA4NjA2OCwxLjAwMDAwMCkiLAogICAgICAgICAgImZyYW1lIiA6ICJ7ezgzLCAxODN9LCB7MjAwLCAyMDB9fSIsCiAgICAgICAgICAiYm9yZGVyX2NvbG9yIiA6ICJSR0JBKDAuMDAwMDAwLDAuMDAwMDAwLDAuMDAwMDAwLDEuMDAwMDAwKSIsCiAgICAgICAgICAiZWRpdGFibGUiIDogZmFsc2UsCiAgICAgICAgICAiYm9yZGVyX3dpZHRoIiA6IDEsCiAgICAgICAgICAidGludF9jb2xvciIgOiAiUkdCQSgxLjAwMDAwMCwwLjAzMTI1MCwwLjAzMTI1MCwxLjAwMDAwMCkiLAogICAgICAgICAgImFsaWdubWVudCIgOiAibGVmdCIsCiAgICAgICAgICAiYXV0b2NvcnJlY3Rpb25fdHlwZSIgOiAiZGVmYXVsdCIsCiAgICAgICAgICAiYWxwaGEiIDogMSwKICAgICAgICAgICJ0ZXh0X2NvbG9yIiA6ICJSR0JBKDEuMDAwMDAwLDAuMDMxMjUwLDAuMDMxMjUwLDEuMDAwMDAwKSIsCiAgICAgICAgICAiZm9udF9uYW1lIiA6ICI8U3lzdGVtPiIsCiAgICAgICAgICAic3BlbGxjaGVja2luZ190eXBlIiA6ICJkZWZhdWx0IiwKICAgICAgICAgICJjbGFzcyIgOiAiVGV4dFZpZXciLAogICAgICAgICAgIm5hbWUiIDogIkRlYnVnTG9nQXJlYSIsCiAgICAgICAgICAiZmxleCIgOiAiV0hMUlRCIgogICAgICAgIH0sCiAgICAgICAgInNlbGVjdGVkIiA6IGZhbHNlCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAibm9kZXMiIDogWwoKICAgICAgICBdLAogICAgICAgICJmcmFtZSIgOiAie3syNTAsIDQ0NH0sIHs4MCwgODR9fSIsCiAgICAgICAgImNsYXNzIiA6ICJCdXR0b24iLAogICAgICAgICJhdHRyaWJ1dGVzIiA6IHsKICAgICAgICAgICJmbGV4IiA6ICJXSExSVEIiLAogICAgICAgICAgImFjdGlvbiIgOiAiTXVzaWNTdG9wIiwKICAgICAgICAgICJpbWFnZV9uYW1lIiA6ICJpb2I6c3RvcF8yNTYiLAogICAgICAgICAgImZyYW1lIiA6ICJ7ezE0MywgMjg0fSwgezgwLCAzMn19IiwKICAgICAgICAgICJ0aXRsZSIgOiAiIiwKICAgICAgICAgICJ1dWlkIiA6ICJGNTE1M0FBOS02Q0VDLTREOTMtOTYyMy1DREU2QTg3MTM2OTEiLAogICAgICAgICAgImNsYXNzIiA6ICJCdXR0b24iLAogICAgICAgICAgImZvbnRfc2l6ZSIgOiAxNSwKICAgICAgICAgICJuYW1lIiA6ICJTdG9wIgogICAgICAgIH0sCiAgICAgICAgInNlbGVjdGVkIiA6IGZhbHNlCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAibm9kZXMiIDogWwoKICAgICAgICBdLAogICAgICAgICJmcmFtZSIgOiAie3szNSwgNDQ0fSwgezgwLCA4NH19IiwKICAgICAgICAiY2xhc3MiIDogIkJ1dHRvbiIsCiAgICAgICAgImF0dHJpYnV0ZXMiIDogewogICAgICAgICAgImZsZXgiIDogIldITFJUQiIsCiAgICAgICAgICAiYWN0aW9uIiA6ICJQbGF5IiwKICAgICAgICAgICJuYW1lIiA6ICJQbGF5IiwKICAgICAgICAgICJmcmFtZSIgOiAie3sxNDMsIDI4NH0sIHs4MCwgMzJ9fSIsCiAgICAgICAgICAidGl0bGUiIDogIiIsCiAgICAgICAgICAidXVpZCIgOiAiRjUxNTNBQTktNkNFQy00RDkzLTk2MjMtQ0RFNkE4NzEzNjkxIiwKICAgICAgICAgICJjbGFzcyIgOiAiQnV0dG9uIiwKICAgICAgICAgICJmb250X3NpemUiIDogMTUsCiAgICAgICAgICAiaW1hZ2VfbmFtZSIgOiAiaW9iOnBsYXlfMjU2IgogICAgICAgIH0sCiAgICAgICAgInNlbGVjdGVkIiA6IGZhbHNlCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAibm9kZXMiIDogWwoKICAgICAgICBdLAogICAgICAgICJmcmFtZSIgOiAie3s2LCA2fSwgezUwLCA1MH19IiwKICAgICAgICAiY2xhc3MiIDogIkJ1dHRvbiIsCiAgICAgICAgImF0dHJpYnV0ZXMiIDogewogICAgICAgICAgImZsZXgiIDogIldITFJUQiIsCiAgICAgICAgICAiYWN0aW9uIiA6ICJDbG9zZSIsCiAgICAgICAgICAiaW1hZ2VfbmFtZSIgOiAiaW9iOmNsb3NlX3JvdW5kXzI1NiIsCiAgICAgICAgICAiZnJhbWUiIDogInt7MTQzLCAyODR9LCB7ODAsIDMyfX0iLAogICAgICAgICAgInRpdGxlIiA6ICIiLAogICAgICAgICAgInV1aWQiIDogIkY1MTUzQUE5LTZDRUMtNEQ5My05NjIzLUNERTZBODcxMzY5MSIsCiAgICAgICAgICAiY2xhc3MiIDogIkJ1dHRvbiIsCiAgICAgICAgICAibmFtZSIgOiAiQ2xvc2UiLAogICAgICAgICAgImZvbnRfc2l6ZSIgOiAxNQogICAgICAgIH0sCiAgICAgICAgInNlbGVjdGVkIiA6IGZhbHNlCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAibm9kZXMiIDogWwoKICAgICAgICBdLAogICAgICAgICJmcmFtZSIgOiAie3sxNDUsIDQ0NH0sIHs4MCwgODR9fSIsCiAgICAgICAgImNsYXNzIiA6ICJCdXR0b24iLAogICAgICAgICJhdHRyaWJ1dGVzIiA6IHsKICAgICAgICAgICJmbGV4IiA6ICJXSExSVEIiLAogICAgICAgICAgImFjdGlvbiIgOiAiUmVwZWF0IiwKICAgICAgICAgICJpbWFnZV9uYW1lIiA6ICJpb2I6aW9zN19yZWZyZXNoX2VtcHR5XzI1NiIsCiAgICAgICAgICAiZnJhbWUiIDogInt7MTQzLCAyODR9LCB7ODAsIDMyfX0iLAogICAgICAgICAgInRpdGxlIiA6ICIiLAogICAgICAgICAgInV1aWQiIDogIkY1MTUzQUE5LTZDRUMtNEQ5My05NjIzLUNERTZBODcxMzY5MSIsCiAgICAgICAgICAiY2xhc3MiIDogIkJ1dHRvbiIsCiAgICAgICAgICAibmFtZSIgOiAiUmVwZWF0IiwKICAgICAgICAgICJmb250X3NpemUiIDogMTUKICAgICAgICB9LAogICAgICAgICJzZWxlY3RlZCIgOiBmYWxzZQogICAgICB9LAogICAgICB7CiAgICAgICAgIm5vZGVzIiA6IFsKCiAgICAgICAgXSwKICAgICAgICAiZnJhbWUiIDogInt7MzUsIDUzNn0sIHs4MCwgMzJ9fSIsCiAgICAgICAgImNsYXNzIiA6ICJMYWJlbCIsCiAgICAgICAgImF0dHJpYnV0ZXMiIDogewogICAgICAgICAgImZsZXgiIDogIldITFJUQiIsCiAgICAgICAgICAibmFtZSIgOiAiIiwKICAgICAgICAgICJ0ZXh0X2NvbG9yIiA6ICJSR0JBKDEuMDAwMDAwLDAuMDMxMjUwLDAuMDMxMjUwLDEuMDAwMDAwKSIsCiAgICAgICAgICAiZnJhbWUiIDogInt7MTA4LCAyODR9LCB7MTUwLCAzMn19IiwKICAgICAgICAgICJ1dWlkIiA6ICI0NERFM0IyOS1CN0M2LTRFMTktQkQzNy1EMjkxNjE0MTlDMTIiLAogICAgICAgICAgImNsYXNzIiA6ICJMYWJlbCIsCiAgICAgICAgICAiYWxpZ25tZW50IiA6ICJjZW50ZXIiLAogICAgICAgICAgInRleHQiIDogIlBsYXkiLAogICAgICAgICAgImZvbnRfc2l6ZSIgOiAxOCwKICAgICAgICAgICJmb250X25hbWUiIDogIjxTeXN0ZW0+IgogICAgICAgIH0sCiAgICAgICAgInNlbGVjdGVkIiA6IGZhbHNlCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAibm9kZXMiIDogWwoKICAgICAgICBdLAogICAgICAgICJmcmFtZSIgOiAie3sxMjMsIDUzNn0sIHsxMTksIDMyfX0iLAogICAgICAgICJjbGFzcyIgOiAiTGFiZWwiLAogICAgICAgICJhdHRyaWJ1dGVzIiA6IHsKICAgICAgICAgICJmbGV4IiA6ICJXSExSVEIiLAogICAgICAgICAgImZvbnRfc2l6ZSIgOiAxOCwKICAgICAgICAgICJmb250X25hbWUiIDogIjxTeXN0ZW0+IiwKICAgICAgICAgICJmcmFtZSIgOiAie3sxMDgsIDI4NH0sIHsxNTAsIDMyfX0iLAogICAgICAgICAgInV1aWQiIDogIjQ0REUzQjI5LUI3QzYtNEUxOS1CRDM3LUQyOTE2MTQxOUMxMiIsCiAgICAgICAgICAiY2xhc3MiIDogIkxhYmVsIiwKICAgICAgICAgICJhbGlnbm1lbnQiIDogImNlbnRlciIsCiAgICAgICAgICAidGV4dCIgOiAiUmVwZWF0IiwKICAgICAgICAgICJuYW1lIiA6ICIiLAogICAgICAgICAgInRleHRfY29sb3IiIDogIlJHQkEoMS4wMDAwMDAsMC4wMzEyNTAsMC4wMzEyNTAsMS4wMDAwMDApIgogICAgICAgIH0sCiAgICAgICAgInNlbGVjdGVkIiA6IGZhbHNlCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAibm9kZXMiIDogWwoKICAgICAgICBdLAogICAgICAgICJmcmFtZSIgOiAie3syNTAsIDUzNn0sIHs4MCwgMzJ9fSIsCiAgICAgICAgImNsYXNzIiA6ICJMYWJlbCIsCiAgICAgICAgImF0dHJpYnV0ZXMiIDogewogICAgICAgICAgImZsZXgiIDogIldITFJUQiIsCiAgICAgICAgICAiZm9udF9zaXplIiA6IDE4LAogICAgICAgICAgImZvbnRfbmFtZSIgOiAiPFN5c3RlbT4iLAogICAgICAgICAgImZyYW1lIiA6ICJ7ezEwOCwgMjg0fSwgezE1MCwgMzJ9fSIsCiAgICAgICAgICAidXVpZCIgOiAiNDRERTNCMjktQjdDNi00RTE5LUJEMzctRDI5MTYxNDE5QzEyIiwKICAgICAgICAgICJjbGFzcyIgOiAiTGFiZWwiLAogICAgICAgICAgImFsaWdubWVudCIgOiAiY2VudGVyIiwKICAgICAgICAgICJ0ZXh0IiA6ICJTdG9wIiwKICAgICAgICAgICJuYW1lIiA6ICIiLAogICAgICAgICAgInRleHRfY29sb3IiIDogIlJHQkEoMS4wMDAwMDAsMC4wMzEyNTAsMC4wMzEyNTAsMS4wMDAwMDApIgogICAgICAgIH0sCiAgICAgICAgInNlbGVjdGVkIiA6IGZhbHNlCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAibm9kZXMiIDogWwoKICAgICAgICBdLAogICAgICAgICJmcmFtZSIgOiAie3s2LCAzMDV9LCB7MzUzLCAzNH19IiwKICAgICAgICAiY2xhc3MiIDogIlNsaWRlciIsCiAgICAgICAgImF0dHJpYnV0ZXMiIDogewogICAgICAgICAgImZsZXgiIDogIldITFJUQiIsCiAgICAgICAgICAiY29udGludW91cyIgOiB0cnVlLAogICAgICAgICAgImZyYW1lIiA6ICJ7ezgzLCAyODN9LCB7MjAwLCAzNH19IiwKICAgICAgICAgICJ0aW50X2NvbG9yIiA6ICJSR0JBKDEuMDAwMDAwLDAuMDMxMjUwLDAuMDMxMjUwLDEuMDAwMDAwKSIsCiAgICAgICAgICAidXVpZCIgOiAiRTZDOEQyREQtOTNCMS00QkNCLUEzODgtMjZENzg1MEM1NUY2IiwKICAgICAgICAgICJjbGFzcyIgOiAiU2xpZGVyIiwKICAgICAgICAgICJ2YWx1ZSIgOiAwLAogICAgICAgICAgIm5hbWUiIDogInNlZWtiYXIiCiAgICAgICAgfSwKICAgICAgICAic2VsZWN0ZWQiIDogdHJ1ZQogICAgICB9LAogICAgICB7CiAgICAgICAgIm5vZGVzIiA6IFsKCiAgICAgICAgXSwKICAgICAgICAiZnJhbWUiIDogInt7NTUsIDZ9LCB7MjE1LCA4MH19IiwKICAgICAgICAiY2xhc3MiIDogIkxhYmVsIiwKICAgICAgICAiYXR0cmlidXRlcyIgOiB7CiAgICAgICAgICAiZmxleCIgOiAiV0hMUlRCIiwKICAgICAgICAgICJuYW1lIiA6ICIiLAogICAgICAgICAgInRleHRfY29sb3IiIDogIlJHQkEoMS4wMDAwMDAsMC4wMzEyNTAsMC4wMzEyNTAsMS4wMDAwMDApIiwKICAgICAgICAgICJmcmFtZSIgOiAie3sxMDgsIDI4NH0sIHsxNTAsIDMyfX0iLAogICAgICAgICAgInRpbnRfY29sb3IiIDogIlJHQkEoMS4wMDAwMDAsMC4wMzEyNTAsMC4wMzEyNTAsMS4wMDAwMDApIiwKICAgICAgICAgICJ1dWlkIiA6ICI4MTI1OEYxQy0yQzAzLTRENDMtQjZEQy1EN0ZGRTRDQTJCMkMiLAogICAgICAgICAgImNsYXNzIiA6ICJMYWJlbCIsCiAgICAgICAgICAiYWxpZ25tZW50IiA6ICJjZW50ZXIiLAogICAgICAgICAgInRleHQiIDogIlJlbW90ZSBNdXNpYyBQbGF5ZXIiLAogICAgICAgICAgImZvbnRfc2l6ZSIgOiAyMiwKICAgICAgICAgICJmb250X25hbWUiIDogIjxTeXN0ZW0tQm9sZD4iCiAgICAgICAgfSwKICAgICAgICAic2VsZWN0ZWQiIDogZmFsc2UKICAgICAgfSwKICAgICAgewogICAgICAgICJub2RlcyIgOiBbCgogICAgICAgIF0sCiAgICAgICAgImZyYW1lIiA6ICJ7ezYsIDYzfSwgezUwLCAyM319IiwKICAgICAgICAiY2xhc3MiIDogIkxhYmVsIiwKICAgICAgICAiYXR0cmlidXRlcyIgOiB7CiAgICAgICAgICAiZmxleCIgOiAiV0hMUlRCIiwKICAgICAgICAgICJuYW1lIiA6ICIiLAogICAgICAgICAgInRleHRfY29sb3IiIDogIlJHQkEoMS4wMDAwMDAsMC4wMzEyNTAsMC4wMzEyNTAsMS4wMDAwMDApIiwKICAgICAgICAgICJmcmFtZSIgOiAie3sxMDgsIDI4NH0sIHsxNTAsIDMyfX0iLAogICAgICAgICAgInV1aWQiIDogIjVFNjkyNTA3LTIzQUUtNDhDMS1CNkNGLTVFMDMwNTZFMDdGRSIsCiAgICAgICAgICAiY2xhc3MiIDogIkxhYmVsIiwKICAgICAgICAgICJhbGlnbm1lbnQiIDogImNlbnRlciIsCiAgICAgICAgICAidGV4dCIgOiAiQ2xvc2UiLAogICAgICAgICAgImZvbnRfc2l6ZSIgOiAxNSwKICAgICAgICAgICJmb250X25hbWUiIDogIjxTeXN0ZW0+IgogICAgICAgIH0sCiAgICAgICAgInNlbGVjdGVkIiA6IGZhbHNlCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAibm9kZXMiIDogWwoKICAgICAgICBdLAogICAgICAgICJmcmFtZSIgOiAie3syNjksIDYzfSwgezkwLCAyMn19IiwKICAgICAgICAiY2xhc3MiIDogIkxhYmVsIiwKICAgICAgICAiYXR0cmlidXRlcyIgOiB7CiAgICAgICAgICAiZmxleCIgOiAiV0hMUlRCIiwKICAgICAgICAgICJuYW1lIiA6ICIiLAogICAgICAgICAgInRleHRfY29sb3IiIDogIlJHQkEoMS4wMDAwMDAsMC4wMzEyNTAsMC4wMzEyNTAsMS4wMDAwMDApIiwKICAgICAgICAgICJmcmFtZSIgOiAie3sxMDgsIDI4NH0sIHsxNTAsIDMyfX0iLAogICAgICAgICAgInV1aWQiIDogIjdFNTM5QUY1LTk2NkItNEU2Mi1BMkRCLUMzNkJCRUE5N0YzNCIsCiAgICAgICAgICAiY2xhc3MiIDogIkxhYmVsIiwKICAgICAgICAgICJhbGlnbm1lbnQiIDogImNlbnRlciIsCiAgICAgICAgICAidGV4dCIgOiAiVm9sbXVlIFN5bmMiLAogICAgICAgICAgImZvbnRfc2l6ZSIgOiAxMywKICAgICAgICAgICJmb250X25hbWUiIDogIjxTeXN0ZW0+IgogICAgICAgIH0sCiAgICAgICAgInNlbGVjdGVkIiA6IGZhbHNlCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAibm9kZXMiIDogWwoKICAgICAgICBdLAogICAgICAgICJmcmFtZSIgOiAie3s2LCA0MDJ9LCB7MzUzLCAzNH19IiwKICAgICAgICAiY2xhc3MiIDogIlNsaWRlciIsCiAgICAgICAgImF0dHJpYnV0ZXMiIDogewogICAgICAgICAgImZsZXgiIDogIldITFJUQiIsCiAgICAgICAgICAiY29udGludW91cyIgOiB0cnVlLAogICAgICAgICAgImFjdGlvbiIgOiAiU2V0U3lzdGVtVm9sdW1lIiwKICAgICAgICAgICJmcmFtZSIgOiAie3s4MywgMjgzfSwgezIwMCwgMzR9fSIsCiAgICAgICAgICAidGludF9jb2xvciIgOiAiUkdCQSgxLjAwMDAwMCwwLjAzMTI1MCwwLjAzMTI1MCwxLjAwMDAwMCkiLAogICAgICAgICAgInV1aWQiIDogIkU2QzhEMkRELTkzQjEtNEJDQi1BMzg4LTI2RDc4NTBDNTVGNiIsCiAgICAgICAgICAiY2xhc3MiIDogIlNsaWRlciIsCiAgICAgICAgICAidmFsdWUiIDogMCwKICAgICAgICAgICJuYW1lIiA6ICJWb2x1bWUiCiAgICAgICAgfSwKICAgICAgICAic2VsZWN0ZWQiIDogZmFsc2UKICAgICAgfSwKICAgICAgewogICAgICAgICJub2RlcyIgOiBbCgogICAgICAgIF0sCiAgICAgICAgImZyYW1lIiA6ICJ7ezI4OCwgMTR9LCB7NTEsIDMxfX0iLAogICAgICAgICJjbGFzcyIgOiAiU3dpdGNoIiwKICAgICAgICAiYXR0cmlidXRlcyIgOiB7CiAgICAgICAgICAiYWN0aW9uIiA6ICJDaGVja2luZ1N5bmMiLAogICAgICAgICAgImZsZXgiIDogIldITFJUQiIsCiAgICAgICAgICAiZnJhbWUiIDogInt7MTU3LCAyODR9LCB7NTEsIDMxfX0iLAogICAgICAgICAgInRpbnRfY29sb3IiIDogIlJHQkEoMS4wMDAwMDAsMC4wMzEyNTAsMC4wMzEyNTAsMS4wMDAwMDApIiwKICAgICAgICAgICJjbGFzcyIgOiAiU3dpdGNoIiwKICAgICAgICAgICJ1dWlkIiA6ICJCNjBGRTQwMC1DRDBBLTRBNDUtQTYxOS0wRkYxMkM4OURBRkUiLAogICAgICAgICAgInZhbHVlIiA6IGZhbHNlLAogICAgICAgICAgIm5hbWUiIDogIlN5bmNWb2xtdW1lIgogICAgICAgIH0sCiAgICAgICAgInNlbGVjdGVkIiA6IGZhbHNlCiAgICAgIH0KICAgIF0sCiAgICAiZnJhbWUiIDogInt7MCwgMH0sIHszNjUsIDU5OX19IiwKICAgICJjbGFzcyIgOiAiVmlldyIsCiAgICAiYXR0cmlidXRlcyIgOiB7CiAgICAgICJmbGV4IiA6ICIiLAogICAgICAiY3VzdG9tX2NsYXNzIiA6ICIiLAogICAgICAiZW5hYmxlZCIgOiB0cnVlLAogICAgICAidGludF9jb2xvciIgOiAiUkdCQSgxLjAwMDAwMCwwLjAzMTI1MCwwLjAzMTI1MCwxLjAwMDAwMCkiLAogICAgICAiYm9yZGVyX2NvbG9yIiA6ICJSR0JBKDAuMDAwMDAwLDAuMDAwMDAwLDAuMDAwMDAwLDEuMDAwMDAwKSIsCiAgICAgICJiYWNrZ3JvdW5kX2NvbG9yIiA6ICJSR0JBKDAuMTMxNzEwLDAuMTMxNzEwLDAuMTMxNzEwLDEuMDAwMDAwKSIsCiAgICAgICJuYW1lIiA6ICJNdXNpY1BsYXllciIKICAgIH0sCiAgICAic2VsZWN0ZWQiIDogZmFsc2UKICB9Cl0=")
NSBundle.bundle(Path="/System/Library/Frameworks/MultipeerConnectivity"
                     ".framework").load()
MCPeerID = ObjCClass('MCPeerID')
MCSession = ObjCClass('MCSession')
MCNearbyServiceAdvertiser = ObjCClass('MCNearbyServiceAdvertiser')
MCNearbyServiceBrowser = ObjCClass('MCNearbyServiceBrowser')
NSRunLoop = ObjCClass('NSRunLoop')
NSDefaultRunLoopMode = ObjCInstance(c_void_p.in_dll(c, "NSDefaultRunLoopMode"))

MCSession.stringForMCSessionSendDataMode_(1)
mc_managers = {}
mc_inputstream_managers = {}

def get_self(manager_object):
    global mc_managers
    return mc_managers.get(
        ObjCInstance(manager_object).myPeerID().hash(),
        None)

def session_peer_didChangeState_(_self,_cmd,_session,_peerID,_state):
    self = get_self(_session)
    if self is None: return
    peerID = ObjCInstance(_peerID)
    peerID.display_name = str(peerID.displayName())
    if _state == 2:
        self._peer_collector(peerID)
    if (_state is None or _state == 0):
        self.peer_removed(peerID)

def session_didReceiveData_fromPeer_(_self, _cmd, _session, _data, _peerID):
    self = get_self(_session)
    if self is None: return
    peer_id = ObjCInstance(_peerID)
    peer_id.display_name = str(peer_id.displayName())
    decoded_data = nsdata_to_bytes(ObjCInstance(_data))
    self.receive(decoded_data, peer_id)

def session_didReceiveStream_withName_fromPeer_(_self, _cmd, _session, _stream,
        _streamName, _peerID):
    self = get_self(_session)
    if self is None: return
    stream = ObjCInstance(_stream)
    peer_id = ObjCInstance(_peerID)
    stream.setDelegate_(ObjCInstance(_self))
    mc_inputstream_managers[stream] = self
    self.peer_per_inputstream[stream] = peer_id
    stream.scheduleInRunLoop_forMode_(NSRunLoop.mainRunLoop(),
        NSDefaultRunLoopMode)
    stream.open()

def stream_handleEvent_(_self, _cmd, _stream, _event):
    if _event == 2:
        buffer = ctypes.create_string_buffer(1024)
        stream = ObjCInstance(_stream)
        read_len = stream.read_maxLength_(buffer, 1024)
        if read_len > 0:
            content = bytearray(buffer[:read_len])
            self = mc_inputstream_managers[stream]
            peer_id = self.peer_per_inputstream[stream]
            self.stream_receive(content, peer_id)

SessionDelegate = create_objc_class('SessionDelegate',
    methods=[session_peer_didChangeState_, session_didReceiveData_fromPeer_,
             session_didReceiveStream_withName_fromPeer_, stream_handleEvent_],
    protocols=['MCSessionDelegate', 'NSStreamDelegate'])
SDelegate = SessionDelegate.alloc().init()

def browser_didNotStartBrowsingForPeers_(_self, _cmd, _browser, _err):
    _print('MultipeerConnectivity framework error')

def browser_foundPeer_withDiscoveryInfo_(_self, _cmd, _browser, _peerID,
        _info):
    self = get_self(_browser)
    if self is None: return

    peerID = ObjCInstance(_peerID)
    browser = ObjCInstance(_browser)
    context = json.dumps(
        self.initial_data).encode() if self.initial_data is not None else None
    browser.invitePeer_toSession_withContext_timeout_(peerID, self.session,
        context, 0)

def browser_lostPeer_(_self, _cmd, browser, peer):
    pass

BrowserDelegate = create_objc_class('BrowserDelegate',
    methods=[browser_foundPeer_withDiscoveryInfo_, browser_lostPeer_,
             browser_didNotStartBrowsingForPeers_],
    protocols=['MCNearbyServiceBrowserDelegate'])
Bdelegate = BrowserDelegate.alloc().init()

class _block_descriptor(Structure):
    _fields_ = [('reserved', c_ulong), ('size', c_ulong),
                ('copy_helper', c_void_p), ('dispose_helper', c_void_p),
                ('signature', c_char_p)]

InvokeFuncType = ctypes.CFUNCTYPE(None, *[c_void_p, ctypes.c_bool, c_void_p])

class _block_literal(Structure):
    _fields_ = [('isa', c_void_p), ('flags', c_int), ('reserved', c_int),
                ('invoke', InvokeFuncType), ('descriptor', _block_descriptor)]

def advertiser_didReceiveInvitationFromPeer_withContext_invitationHandler_(
        _self, _cmd, _advertiser, _peerID, _context, _invitationHandler):
    self = get_self(_advertiser)
    if self is None: return
    peer_id = ObjCInstance(_peerID)
    if _context is not None:
        decoded_data = nsdata_to_bytes(ObjCInstance(_context)).decode()
        initial_data = json.loads(decoded_data)
        self.initial_peer_data[peer_id.hash()] = initial_data
    peer_id.display_name = str(peer_id.displayName())
    self._peer_collector(peer_id)
    invitation_handler = ObjCInstance(_invitationHandler)
    retain_global(invitation_handler)
    blk = _block_literal.from_address(_invitationHandler)
    blk.invoke(invitation_handler, True, self.session)

f = advertiser_didReceiveInvitationFromPeer_withContext_invitationHandler_
f.argtypes = [c_void_p] * 4
f.restype = None
f.encoding = b'v@:@@@@?'
AdvertiserDelegate = create_objc_class('AdvertiserDelegate', methods=[
    advertiser_didReceiveInvitationFromPeer_withContext_invitationHandler_])
ADelegate = AdvertiserDelegate.alloc().init()

class MultipeerConnectivity():
    def __init__(self, display_name='Peer', service_type='dev-srv',
            initial_data=None, initialize_streams=False):
        global mc_managers
    
        if display_name is None or display_name == '' or len(
                display_name.encode()) > 63:
            raise ValueError(
                'display_name must not be None or empty string, and must be at '
                'most 63 bytes long (UTF-8 encoded)', display_name)
    
        self.service_type = service_type
        check_re = re.compile(r'[^a-z0-9\-.]')
        check_str = check_re.search(self.service_type)
        if len(self.service_type) < 1 or len(self.service_type) > 15 or bool(
                check_str):
            raise ValueError(
                'service_type must be 1-15 characters long and can contain only '
                'ASCII lowercase letters, numbers and hyphens', service_type)

        self.my_id = MCPeerID.alloc().initWithDisplayName(display_name)
        self.my_id.display_name = str(self.my_id.displayName())

        self.initial_data = initial_data
        self.initial_peer_data = {}
        self._peer_connection_hit_count = {}

        mc_managers[self.my_id.hash()] = self

        self.initialize_streams = initialize_streams
        self.outputstream_per_peer = {}
        self.peer_per_inputstream = {}

        self.session = MCSession.alloc().initWithPeer_(self.my_id)
        self.session.setDelegate_(SDelegate)

        self.browser = MCNearbyServiceBrowser.alloc().initWithPeer_serviceType_(
            self.my_id, self.service_type)
        self.browser.setDelegate_(Bdelegate)

        self.advertiser = MCNearbyServiceAdvertiser.alloc().\
            initWithPeer_discoveryInfo_serviceType_(
                self.my_id, ns({}), self.service_type)
        self.advertiser.setDelegate_(ADelegate)

        self.start_looking_for_peers()

    def peer_added(self, peer_id):
        _print('Added peer {}'.format(peer_id.display_name))

    def peer_removed(self, peer_id):
        _print('Removed peer {}'.format(peer_id.display_name))

    def get_peers(self):
        peer_list = []
        for peer in self.session.connectedPeers():
            peer.display_name = str(peer.displayName())
            peer_list.append(peer)
        return peer_list

    def get_initial_data(self, peer_id):
        return self.initial_peer_data.get(peer_id.hash(), None)

    def start_looking_for_peers(self):
        self.browser.startBrowsingForPeers()
        self.advertiser.startAdvertisingPeer()

    def stop_looking_for_peers(self):
        self.advertiser.stopAdvertisingPeer()
        self.browser.stopBrowsingForPeers()

    def send(self, message, to_peer=None, reliable=True):
        if type(to_peer) == list:
            peers = to_peer
        elif to_peer is None:
            peers = self.get_peers()
        else:
            peers = [to_peer]
        send_mode = 0 if reliable else 1
        self.session.sendData_toPeers_withMode_error_(message, peers, send_mode, None)
        if b'Volume' in message:
            _print('Volume Setting Mode!\nPlease ReTry Play Button!')
        else:
            _print('command / data sended!')

    def stream(self, byte_data, to_peer=None):
        if type(to_peer) == list:
            peers = to_peer
        elif to_peer is None:
            peers = self.get_peers()
        else:
            peers = [to_peer]
        for peer_id in peers:
            peer_id = ObjCInstance(peer_id)
            stream = self.outputstream_per_peer.get(peer_id.hash(), None)
            if stream is None:
                stream = self._set_up_stream(peer_id)
            data_len = len(byte_data)
            wrote_len = stream.write_maxLength_(byte_data, data_len)
            if wrote_len != data_len:
                _print(f'Error writing data, wrote {wrote_len}/{data_len} bytes')

    def _set_up_stream(self, to_peer):
        output_stream = ObjCInstance(
            self.session.startStreamWithName_toPeer_error_('stream', to_peer,
                None))
        output_stream.setDelegate_(SDelegate)
        output_stream.scheduleInRunLoop_forMode_(NSRunLoop.mainRunLoop(),
            NSDefaultRunLoopMode)
        output_stream.open()
        self.outputstream_per_peer[to_peer.hash()] = output_stream
        return output_stream

    def receive(self, message, from_peer):
        global p
        try:
            if message.decode().split(',')[0] == 'Volume':
               ClientSetVolume(float(message.decode(errors='ignore').split(',')[1]))
        except:
            _print('')
        if message == b'Received':
            Seekbar = SeekbarThread()
            Seekbar.setDaemon(True)
            seekbarThreadList.append(Seekbar)
            ReceiveM[0] = message
            _print('NowPlaying....{}'.format(MusicPath[0]))
            p = sound.Player(MusicPath[0])
            MusicParent[0] = p
            try:
                NowClosed[0] = '1'
                Seekbar.kill()
            except:
                pass
            NowClosed[0] = '0'
            Seekbar.start()
            p.stop()
            p.play()
            PlayDetect[0] = '1'
            ReceiveM[0] = b''
        elif message == b'mstop':
            ReceiveM[0] = message
            _print('Stopping.......')
            p = sound.Player('tmp/tmp.m4a')
            MusicParent[0] = p
            p.stop()
            self.send(b'FStop')
        elif message == b'FStop':
            ReceiveM[0] = message
            _print('Stopping.......')
            p = sound.Player(MusicPath[0])
            MusicParent[0] = p
            p.stop()
        else:
            try:
                if not message.decode().split(',')[0] == 'Volume':
                    Seekbar = SeekbarThread()
                    Seekbar.setDaemon(True)
                    seekbarThreadList.append(Seekbar)
                    ReceiveM[0] = message
                    with open('tmp/tmp.m4a', 'wb') as Ff:
                        Ff.write(message)
                    self.send(b'Received')
                    time.sleep(0.08)
                    p = sound.Player('tmp/tmp.m4a')
                    MusicParent[0] = p
                    try:
                        NowClosed[0] = '1'
                        Seekbar.kill()
                    except:
                        pass
                    NowClosed[0] = '0'
                    Seekbar.start()
                    if p.playing:
                        p.stop()
                        _print('NowPlaying....')
                        p.play()
                        ReceiveM[0] = b''
                        PlayDetect[0] = '1'
                    else:
                        _print('NowPlaying....')
                        p.play()
                        ReceiveM[0] = b''
                        PlayDetect[0] = '1'
                else:
                    _print('Volume Setting Mode!\nPlease ReTry Play Button!')
            except:
                Seekbar = SeekbarThread()
                Seekbar.setDaemon(True)
                seekbarThreadList.append(Seekbar)
                ReceiveM[0] = message
                with open('tmp/tmp.m4a', 'wb') as Ff:
                    Ff.write(message)
                self.send(b'Received')
                time.sleep(0.08)
                p = sound.Player('tmp/tmp.m4a')
                MusicParent[0] = p
                try:
                    NowClosed[0] = '1'
                    Seekbar.kill()
                except:
                    pass
                NowClosed[0] = '0'
                Seekbar.start()
                if p.playing:
                    p.stop()
                    _print('NowPlaying....')
                    p.play()
                    ReceiveM[0] = b''
                    PlayDetect[0] = '1'
                else:
                    _print('NowPlaying....')
                    p.play()
                    ReceiveM[0] = b''
                    PlayDetect[0] = '1'

    def stream_receive(self, byte_data, from_peer):
        pass

    def disconnect(self):
        self.session.disconnect()

    def end_all(self):
        self.stop_looking_for_peers()
        self.disconnect()
        RemotePlayer.close()
        sys.exit(0)

    def _peer_collector(self, peer_id):
        peer_hash = peer_id.hash()
        self._peer_connection_hit_count.setdefault(peer_hash, 0)
        self._peer_connection_hit_count[peer_hash] += 1
        if self._peer_connection_hit_count[peer_hash] > 1:
            if (self.initialize_streams and peer_hash not in
                    self.outputstream_per_peer):
                self._set_up_stream(peer_id)
            self.peer_added(peer_id)

def init():
    os.makedirs(os.path.join(os.environ['HOME'], 'Documents', 'InputAudioFiles'), exist_ok=True)
    os.chdir(os.path.join(os.environ['HOME'], 'Documents', 'InputAudioFiles'))
    os.makedirs('tmp', exist_ok=True)
    fs = open('tmp/tmp.m4a', 'wb')
    try:
        fs.write(1)
    except:
        pass

def LoadMusicFiles(MuiscView):
    global dpath, mDirName
    try:
        if MuiscView['MusicList'].data_source.items[0] == '':
            del MuiscView['MusicList'].data_source.items[0]
    except:
        pass
    if not ''.join(MuiscView['MusicList'].data_source.items) == '':
        try:
            ML = [0]
            for u in ML:
                for ul in range(len(MuiscView['MusicList'].data_source.items)):
                    try:
                        del MuiscView['MusicList'].data_source.items[ul]
                    except:
                        ML.append(u+1)
                if ''.join(MuiscView['MusicList'].data_source.items) == '':
                    break
        except:
            pass
    try:
        MFiles = sorted(os.listdir('./'))
        for files in MFiles:
            if os.path.isfile(files):
                listFiles.append(files)
            elif os.path.islink(files):
                listDirs.append(files)
            else:
                listDirs.append(files)
        musics = []
        for mff in MusicFinder('./'):
            for mfile in mff:
                if os.path.isfile(mfile):
                    musics.append(mfile)
        MusicFiles = []
        for mf in range(len(sorted(musics))):
            mDirName.append(str(sorted(musics)[mf].split(sorted(musics)[mf].split('/')[-1])[0]))
            MusicFiles.append(str(sorted(musics)[mf].split('/')[-1]))
        MuiscView['MusicList'].data_source.items = MusicFiles
    except:
        pass

def MusicFinder(dir):
    for root, _, file in os.walk('./'):
        yield file
        for musicFile in file:
            if musicFile.split('.')[-1].lower() == 'm4a':
                yield os.path.join(root, musicFile)

def SelectFile(file):
    global MusicFileName, FileIndex
    try:
        FileIndex = file.selected_row
        MusicFileName = file.items[FileIndex]
    except:
        MusicFileName = ''

def RepeatLoop(MBytes):
    try:
        P = p
    except:
        P = sound.Player(MusicPath[0])
    if P.playing:
        if not MBytes == b'':
            MusicData[0] = MBytes
        P.stop()
        Player.send(b'mstop')
    else:
       PlayDetect[0] = '0'
    while True:
        if LoopBreak[0]:
            break
        else:
            pass
        try:
            P = p
        except:
            P = sound.Player(MusicPath[0])
        if RepeatDetect[0] == '0':
            break
        else:
            pass
        try:
            if P.playing:
                time.sleep(5)
            else:
                time.sleep(1)
            if P.playing and not ReceiveM[0] == b'Received' and PlayDetect[0] == '1':
                StopResending[0] = '0'
                PlayDetect[0] = '0'
            elif not P.playing and not ReceiveM[0] == b'Received' and PlayDetect[0] == '0' and StopResending[0] == '0':
                Player.send(MusicData[0])
                StopResending[0] = '1'
            elif not P.playing and StopResending[0] == '0' and PlayDetect[0] == '0':
                P.stop()
                Player.send(b'mstop')
                Player.send(MusicData[0])
                StopResending[0] = '1'
            else:
                pass
        except:
            pass

class LoopRepeatThread(threading.Thread):
    def __init__(self, Music):
        super().__init__()
        self.started = threading.Event()
        self.Music = Music
        self.alive = True

    def __del__(self):
        try:
            self.kill()
        except:
            pass

    def kill(self):
        self.started.set()
        self.alive = False
        self.started.clear()

    def run(self):
        RepeatLoop(self.Music)

def Play(_):
    if RepeatDetect[0] == '1':
        PlayDetect[0] = '0'
        StopResending[0] = '0'
        _print('ReSending Music Data......')
        Music = open(MusicFileName, 'rb').read()
        MusicData[0] = Music
        LoopMusic = LoopRepeatThread(Music)
        MusicPath[0] = MusicFileName
        if CheckSync[0] == '1':
            Player.send('Volume,{}'.format(round(Control[0][0].value(), 2)).encode('utf-8'))
            CheckSync[0] = '0'
            RemotePlayer['SyncVolmume'].value = 0
        else:
            try:
                LoopMusic.kill()
                LoopBreak[0] = True
                Player.send(b'mstop')
            except:
                pass
            LoopMusic.setDaemon(True)
            LoopBreak[0] = False
            LoopMusic.start()
            RepeatThread.append(LoopMusic)
    elif RepeatDetect[0] == '0':
        _print('Sending Music Data......')
        Music = open(MusicFileName, 'rb').read()
        MusicPath[0] = MusicFileName
        if CheckSync[0] == '1':
            Player.send('Volume,{}'.format(round(Control[0][0].value(), 2)).encode('utf-8'))
            CheckSync[0] = '0'
            RemotePlayer['SyncVolmume'].value = 0
        else:
            try:
                Player.send(b'mstop')
            except:
                pass
            Player.send(Music)

class SeekbarThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.started = threading.Event()
        self.alive = True

    def __del__(self):
        try:
            self.kill()
        except:
            pass

    def kill(self):
        self.started.set()
        self.alive = False
        self.started.clear()
        self.join(0)

    def run(self):
        while True:
            if NowClosed[0] == '1':
                break
            try:
                P = p
            except:
                P = sound.Player(MusicPath[0])
            try:
                RemotePlayer['seekbar'].value = int(str(P.current_time).split('.')[0]) /  int(str(P.duration).split('.')[0])
                if P.playing:
                    time.sleep(1)
                else:
                    time.sleep(0.3)
            except:
                time.sleep(0.3)
                pass

def Close(_):
    LoopBreak[0] = True
    NowClosed[0] = '1'
    try:
        for T in RepeatThread:
            try:
                T.join(0)
                T.kill()
            except:
                continue
    except:
        pass
    try:
        P = p
    except:
        if not MusicPath[0] == '':
            P = sound.Player(MusicPath[0])
        else:
            MusicPath[0] = 'tmp/tmp.m4a'
            P = sound.Player(MusicPath[0])
    P.stop()
    try:
        for E in seekbarThreadList:
            try:
                E.join(0)
                E.kill()
            except:
                continue
    except:
        pass
    Player.send(b'mstop')
    Player.end_all()

def MusicStop(_):
    Player.send(b'mstop')
    PlayDetect[0] = '0'
    LoopBreak[0] = True
    MusicData[0] = b''
    try:
        MusicParent[0].stop()
    except:
        try:
            if not MusicPath[0] == '':
                p = sound.Player(MusicPath[0])
                p.stop()
            else:
                MusicPath[0] = 'tmp/tmp.m4a'
                p = sound.Player(MusicPath[0])
                p.stop()
        except:
            sys.exit(0)

def _print(view):
    RemotePlayer['DebugLogArea'].text = view

def Repeat(v):
    if RepeatDetect[0] == '0':
        v.superview['Repeat'].image = ui.Image('iob:ios7_refresh_256')
        RepeatDetect[0] = '1'
    elif RepeatDetect[0] == '1':
        v.superview['Repeat'].image = ui.Image('iob:ios7_refresh_empty_256')
        RepeatDetect[0] = '0'

def SetSystemVolume(Volume):
   for Vol in Control[0]:
        if Vol.isKindOfClass_(ObjCClass('UISlider')):
            Vol.value = round(Volume.value, 2)
            break

def ClientSetVolume(volume):
    for Vols in Control[0]:
        if Vols.isKindOfClass_(ObjCClass('UISlider')):
            Vols.value = round(volume, 2)
            RemotePlayer['Volume'].value = round(volume, 2)
            break

def CheckingSync(V):
    if V.value:
        CheckSync[0] = '1'
    elif not V.value:
        CheckSync[0] = '0'

def main():
    global Player, RemotePlayer
    init()
    time.sleep(0.3)
    RemotePlayer = ui.load_view_str(UIs)
    DeviceName = platform.uname().node
    Player = MultipeerConnectivity(display_name=DeviceName, service_type='music', initial_data=platform.platform())
    LoadMusicFiles(RemotePlayer)
    RemotePlayer.present('panel')
    RemotePlayer['Volume'].value = Control[0][0].value()

if __name__ == '__main__':
    main()
