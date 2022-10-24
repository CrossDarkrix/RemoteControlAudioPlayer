import ui, sound, ctypes, re, json, heapq, base64, os, time, sys, platform
from objc_util import *

listFiles = []
listDirs = []
mDirName = []
MusicPath = ['']
MusicParent = ['']
UIs = base64.b64decode("WwogIHsKICAgICJub2RlcyIgOiBbCiAgICAgIHsKICAgICAgICAibm9kZXMiIDogWwoKICAgICAgICBdLAogICAgICAgICJmcmFtZSIgOiAie3syMSwgNn0sIHszMjUsIDM5MH19IiwKICAgICAgICAiY2xhc3MiIDogIlRhYmxlVmlldyIsCiAgICAgICAgImF0dHJpYnV0ZXMiIDogewogICAgICAgICAgInV1aWQiIDogIjk5ODk3RDJDLTYwOTMtNEU4Qy1CQkE4LTQ5MzFFNDAxQTZGRiIsCiAgICAgICAgICAiZGF0YV9zb3VyY2VfYWN0aW9uIiA6ICJTZWxlY3RGaWxlIiwKICAgICAgICAgICJiYWNrZ3JvdW5kX2NvbG9yIiA6ICJSR0JBKDAuMTI5MzA4LDAuMTI5MzA4LDAuMTI5MzA4LDEuMDAwMDAwKSIsCiAgICAgICAgICAiZnJhbWUiIDogInt7ODMsIDE4M30sIHsyMDAsIDIwMH19IiwKICAgICAgICAgICJkYXRhX3NvdXJjZV9pdGVtcyIgOiAiIiwKICAgICAgICAgICJ0aW50X2NvbG9yIiA6ICJSR0JBKDEuMDAwMDAwLDAuMDMxMjUwLDAuMDMxMjUwLDEuMDAwMDAwKSIsCiAgICAgICAgICAiZGF0YV9zb3VyY2VfbnVtYmVyX29mX2xpbmVzIiA6IDEsCiAgICAgICAgICAiZGF0YV9zb3VyY2VfZGVsZXRlX2VuYWJsZWQiIDogZmFsc2UsCiAgICAgICAgICAiZGF0YV9zb3VyY2VfZm9udF9zaXplIiA6IDE4LAogICAgICAgICAgInJvd19oZWlnaHQiIDogNDQsCiAgICAgICAgICAiY2xhc3MiIDogIlRhYmxlVmlldyIsCiAgICAgICAgICAibmFtZSIgOiAiTXVzaWNMaXN0IiwKICAgICAgICAgICJmbGV4IiA6ICJMUlRCIgogICAgICAgIH0sCiAgICAgICAgInNlbGVjdGVkIiA6IGZhbHNlCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAibm9kZXMiIDogWwoKICAgICAgICBdLAogICAgICAgICJmcmFtZSIgOiAie3syMSwgMzg5fSwgezMyNSwgNDd9fSIsCiAgICAgICAgImNsYXNzIiA6ICJUZXh0VmlldyIsCiAgICAgICAgImF0dHJpYnV0ZXMiIDogewogICAgICAgICAgInV1aWQiIDogIjk1QjAzNEY1LTIwOTItNDBFQS04MjU5LTNFMjU1RjM4ODMyNiIsCiAgICAgICAgICAiZm9udF9zaXplIiA6IDE3LAogICAgICAgICAgImNvcm5lcl9yYWRpdXMiIDogMSwKICAgICAgICAgICJiYWNrZ3JvdW5kX2NvbG9yIiA6ICJSR0JBKDAuMDg2MDY4LDAuMDg2MDY4LDAuMDg2MDY4LDEuMDAwMDAwKSIsCiAgICAgICAgICAiZnJhbWUiIDogInt7ODMsIDE4M30sIHsyMDAsIDIwMH19IiwKICAgICAgICAgICJib3JkZXJfY29sb3IiIDogIlJHQkEoMC4wMDAwMDAsMC4wMDAwMDAsMC4wMDAwMDAsMS4wMDAwMDApIiwKICAgICAgICAgICJlZGl0YWJsZSIgOiBmYWxzZSwKICAgICAgICAgICJib3JkZXJfd2lkdGgiIDogMSwKICAgICAgICAgICJ0aW50X2NvbG9yIiA6ICJSR0JBKDEuMDAwMDAwLDAuMDMxMjUwLDAuMDMxMjUwLDEuMDAwMDAwKSIsCiAgICAgICAgICAiYWxpZ25tZW50IiA6ICJsZWZ0IiwKICAgICAgICAgICJhdXRvY29ycmVjdGlvbl90eXBlIiA6ICJkZWZhdWx0IiwKICAgICAgICAgICJhbHBoYSIgOiAxLAogICAgICAgICAgInRleHRfY29sb3IiIDogIlJHQkEoMS4wMDAwMDAsMC4wMzEyNTAsMC4wMzEyNTAsMS4wMDAwMDApIiwKICAgICAgICAgICJmb250X25hbWUiIDogIjxTeXN0ZW0+IiwKICAgICAgICAgICJzcGVsbGNoZWNraW5nX3R5cGUiIDogImRlZmF1bHQiLAogICAgICAgICAgImNsYXNzIiA6ICJUZXh0VmlldyIsCiAgICAgICAgICAibmFtZSIgOiAiRGVidWdMb2dBcmVhIiwKICAgICAgICAgICJmbGV4IiA6ICJMUlRCIgogICAgICAgIH0sCiAgICAgICAgInNlbGVjdGVkIiA6IGZhbHNlCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAibm9kZXMiIDogWwoKICAgICAgICBdLAogICAgICAgICJmcmFtZSIgOiAie3syMSwgNDQ0fSwgezMyNSwgMzJ9fSIsCiAgICAgICAgImNsYXNzIiA6ICJUZXh0RmllbGQiLAogICAgICAgICJhdHRyaWJ1dGVzIiA6IHsKICAgICAgICAgICJ1dWlkIiA6ICJEMTM4QjIxMy1FRkQ2LTQ2NEItQTVDNi0xQ0ZDNjFDMzYxM0MiLAogICAgICAgICAgImZvbnRfc2l6ZSIgOiAxNywKICAgICAgICAgICJiYWNrZ3JvdW5kX2NvbG9yIiA6ICJSR0JBKDAuMTMwNTA5LDAuMTMwNTA5LDAuMTMwNTA5LDEuMDAwMDAwKSIsCiAgICAgICAgICAiZnJhbWUiIDogInt7ODMsIDI4NH0sIHsyMDAsIDMyfX0iLAogICAgICAgICAgInRpbnRfY29sb3IiIDogIlJHQkEoMS4wMDAwMDAsMC4wMzEyNTAsMC4wMzEyNTAsMS4wMDAwMDApIiwKICAgICAgICAgICJhbGlnbm1lbnQiIDogImxlZnQiLAogICAgICAgICAgImF1dG9jb3JyZWN0aW9uX3R5cGUiIDogImRlZmF1bHQiLAogICAgICAgICAgInRleHQiIDogIlVua25vd0RldmljZSIsCiAgICAgICAgICAicGxhY2Vob2xkZXIiIDogIkRldmljZSBOYW1lIiwKICAgICAgICAgICJ0ZXh0X2NvbG9yIiA6ICJSR0JBKDEuMDAwMDAwLDAuMDMxMjUwLDAuMDMxMjUwLDEuMDAwMDAwKSIsCiAgICAgICAgICAiZm9udF9uYW1lIiA6ICI8U3lzdGVtPiIsCiAgICAgICAgICAic3BlbGxjaGVja2luZ190eXBlIiA6ICJkZWZhdWx0IiwKICAgICAgICAgICJjbGFzcyIgOiAiVGV4dEZpZWxkIiwKICAgICAgICAgICJuYW1lIiA6ICJEZXZpY2VOYW1lIiwKICAgICAgICAgICJmbGV4IiA6ICJMUlRCIgogICAgICAgIH0sCiAgICAgICAgInNlbGVjdGVkIiA6IHRydWUKICAgICAgfSwKICAgICAgewogICAgICAgICJub2RlcyIgOiBbCgogICAgICAgIF0sCiAgICAgICAgImZyYW1lIiA6ICJ7ezI1NSwgNDg0fSwgezgwLCA4NH19IiwKICAgICAgICAiY2xhc3MiIDogIkJ1dHRvbiIsCiAgICAgICAgImF0dHJpYnV0ZXMiIDogewogICAgICAgICAgImZsZXgiIDogIkxSVEIiLAogICAgICAgICAgImFjdGlvbiIgOiAiTXVzaWNTdG9wIiwKICAgICAgICAgICJpbWFnZV9uYW1lIiA6ICJpb2I6c3RvcF8yNTYiLAogICAgICAgICAgImZyYW1lIiA6ICJ7ezE0MywgMjg0fSwgezgwLCAzMn19IiwKICAgICAgICAgICJ0aXRsZSIgOiAiIiwKICAgICAgICAgICJ1dWlkIiA6ICJGNTE1M0FBOS02Q0VDLTREOTMtOTYyMy1DREU2QTg3MTM2OTEiLAogICAgICAgICAgImNsYXNzIiA6ICJCdXR0b24iLAogICAgICAgICAgImZvbnRfc2l6ZSIgOiAxNSwKICAgICAgICAgICJuYW1lIiA6ICJTdG9wIgogICAgICAgIH0sCiAgICAgICAgInNlbGVjdGVkIiA6IGZhbHNlCiAgICAgIH0sCiAgICAgIHsKICAgICAgICAibm9kZXMiIDogWwoKICAgICAgICBdLAogICAgICAgICJmcmFtZSIgOiAie3s4MywgNDg0fSwgezgwLCA4NH19IiwKICAgICAgICAiY2xhc3MiIDogIkJ1dHRvbiIsCiAgICAgICAgImF0dHJpYnV0ZXMiIDogewogICAgICAgICAgImZsZXgiIDogIkxSVEIiLAogICAgICAgICAgImFjdGlvbiIgOiAiUGxheSIsCiAgICAgICAgICAibmFtZSIgOiAiUGxheSIsCiAgICAgICAgICAiZnJhbWUiIDogInt7MTQzLCAyODR9LCB7ODAsIDMyfX0iLAogICAgICAgICAgInRpdGxlIiA6ICIiLAogICAgICAgICAgInV1aWQiIDogIkY1MTUzQUE5LTZDRUMtNEQ5My05NjIzLUNERTZBODcxMzY5MSIsCiAgICAgICAgICAiY2xhc3MiIDogIkJ1dHRvbiIsCiAgICAgICAgICAiZm9udF9zaXplIiA6IDE1LAogICAgICAgICAgImltYWdlX25hbWUiIDogImlvYjpwbGF5XzI1NiIKICAgICAgICB9LAogICAgICAgICJzZWxlY3RlZCIgOiBmYWxzZQogICAgICB9CiAgICBdLAogICAgImZyYW1lIiA6ICJ7ezAsIDB9LCB7MzY1LCA1OTl9fSIsCiAgICAiY2xhc3MiIDogIlZpZXciLAogICAgImF0dHJpYnV0ZXMiIDogewogICAgICAiZmxleCIgOiAiIiwKICAgICAgImN1c3RvbV9jbGFzcyIgOiAiIiwKICAgICAgImVuYWJsZWQiIDogdHJ1ZSwKICAgICAgInRpbnRfY29sb3IiIDogIlJHQkEoMS4wMDAwMDAsMC4wMzEyNTAsMC4wMzEyNTAsMS4wMDAwMDApIiwKICAgICAgImJvcmRlcl9jb2xvciIgOiAiUkdCQSgwLjAwMDAwMCwwLjAwMDAwMCwwLjAwMDAwMCwxLjAwMDAwMCkiLAogICAgICAiYmFja2dyb3VuZF9jb2xvciIgOiAiUkdCQSgwLjEzMTcxMCwwLjEzMTcxMCwwLjEzMTcxMCwxLjAwMDAwMCkiLAogICAgICAibmFtZSIgOiAiTXVzaWNQbGF5ZXIiCiAgICB9LAogICAgInNlbGVjdGVkIiA6IGZhbHNlCiAgfQpd")
NSBundle.bundle(Path="/System/Library/Frameworks/MultipeerConnectivity"
                     ".framework").load()
MCPeerID = ObjCClass('MCPeerID')
MCSession = ObjCClass('MCSession')
MCNearbyServiceAdvertiser = ObjCClass('MCNearbyServiceAdvertiser')
MCNearbyServiceBrowser = ObjCClass('MCNearbyServiceBrowser')
NSRunLoop = ObjCClass('NSRunLoop')
NSDefaultRunLoopMode = ObjCInstance(c_void_p.in_dll(c, "NSDefaultRunLoopMode"))

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
    if _event == 2:  # hasBytesAvailable
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
        if message == b'Received':
            _print('NowPlaying....{}'.format(MusicPath[0]))
            p = sound.Player(MusicPath[0])
            MusicParent[0] = p
            p.stop()
            p.play()
        elif message == b'mstop':
            _print('Stopping.......')
            p = sound.Player('tmp/tmp.m4a')
            MusicParent[0] = p
            p.stop()
            self.send(b'FStop')
        elif message == b'FStop':
            print('Stopping.......')
            p = sound.Player(MusicPath[0])
            MusicParent[0] = p
            p.stop()
        else:
            with open('tmp/tmp.m4a', 'wb') as Ff:
                Ff.write(message)
            self.send(b'Received')
            time.sleep(0.2)
            p = sound.Player('tmp/tmp.m4a')
            MusicParent[0] = p
            if p.playing:
                p.stop()
                _print('NowPlaying....')
                p.play()
            else:
                _print('NowPlaying....')
                p.play()

    def stream_receive(self, byte_data, from_peer):
        pass

    def disconnect(self):
        self.session.disconnect()

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
    os.makedirs('tmp', exist_ok=True) # save receive data dir
    fs = open('tmp/tmp.m4a', 'wb') # init data file
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

def Play(_):
    _print('Sending Music Data......')
    Music = open(MusicFileName, 'rb').read()
    Player.send(Music)
    MusicPath[0] = MusicFileName

def MusicStop(_):
    Player.send(b'mstop')
    try:
        MusicParent[0].stop()
    except:
        try:
            p = sound.Player(MusicPath[0])
            p.stop()
        except:
            sys.exit(0)

def _print(view):
    RemotePlayer['DebugLogArea'].text = view

def main():
    global Player, RemotePlayer
    init()
    RemotePlayer = ui.load_view_str(UIs)
    RemotePlayer['DeviceName'].text = platform.uname().node
    DeviceName = RemotePlayer['DeviceName'].text
    Player = MultipeerConnectivity(display_name=DeviceName, service_type='music', initial_data=platform.platform())
    LoadMusicFiles(RemotePlayer)
    RemotePlayer.present('panel')

if __name__ == '__main__':
    main()

