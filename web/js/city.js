/**
 * @author max
 */

//<![CDATA[
		
		// wait until all the resources are loaded
		window.addEventListener("load", findSVGElements, false);
		
		// fetches the document for the given embedding_element
		function getSubDocument(embedding_element) {
			if (embedding_element.contentDocument) 
			{
				return embedding_element.contentDocument;
			} 
			else 
			{
				var subdoc = null;
				try {
					subdoc = embedding_element.getSVGDocument();
				} catch(e) {}
				return subdoc;
			}
		}
				
		function findSVGElements() {
			var board = document.getElementById("board");
			var subdoc = getSubDocument(board);
				if (subdoc)
					for (i = 0; i < 48; i++) {
						var city = subdoc.getElementById(String(i));
							city.addEventListener("mouseover", function() { this.setAttribute('stroke', 'lime') });
							city.addEventListener("mouseout", function() { this.setAttribute('stroke', 'ivory') ));
					}
		}
		//]]>

	
