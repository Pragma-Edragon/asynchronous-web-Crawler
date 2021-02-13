import re

text = """<script>$('#searchbox').show(0);</script>
        </div>
      </div>
      <div class="clearer"></div>
    </div>
    <div class="footer">
      &copy;2013-2020, aiohttp maintainers.
      
      |
      Powered by <a href="http://sphinx-doc.org/">Sphinx 3.3.1</a>
      
      |
      <a href="_sources/client_reference.rst.txt"
          rel="nofollow">Page source</a>
    </div>

    
    <a href="https://github.com/aio-libs/aiohttp" class="github">
        <img style="position: absolute; top: 0; right: 0; border: 0;" src="https://s3.amazonaws.com/github/ribbons/forkme_right_darkblue_121621.png" alt="Fork me on GitHub"  class="github"/>
    </a>
    

    
  </body>
</html>"""

rePattern = re.compile(r'^https?:/{2,}\S+')
print(re.findall(pattern=rePattern, string=text))