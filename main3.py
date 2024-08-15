from app.FileLoader import load_file
from app.TextSearcher import TextSearcher

if __name__ == '__main__':
    text_searcher = TextSearcher()
    search_phrase = 'what is rba'
    text_searcher.set_search_phrase(search_phrase)
    # sentences = text_searcher.tokenize_into_sentences(load_file('data.txt'))
    sentences = [ "Since 2007, the RBA's outstanding reputation has been affected by the 'Securency' or NPA scandal. These RBA subsidiaries were involved in bribing overseas officials so that Australia might win lucrative note-printing contracts. The assets of the bank include the gold and foreign exchange reserves of Australia, which is estimated to have a net worth of A$101 billion. Nearly 94% of the RBA's employees work at its headquarters in Sydney, New South Wales and at the Business Resumption Site.", "The Reserve Bank of Australia (RBA) came into being on 14 January 1960 as Australia 's central bank and banknote issuing authority, when the Reserve Bank Act 1959 removed the central banking functions from the Commonwealth Bank. The assets of the bank include the gold and foreign exchange reserves of Australia, which is estimated to have a net worth of A$101 billion. Nearly 94% of the RBA's employees work at its headquarters in Sydney, New South Wales and at the Business Resumption Site.", "RBA Recognized with the 2014 Microsoft US Regional Partner of the ... by PR Newswire. Contract Awarded for supply and support the. Securitisations System used for risk management and analysis. ", "The inner workings of a rebuildable atomizer are surprisingly simple. The coil inside the RBA is made of some type of resistance wire, normally Kanthal or nichrome. When a current is applied to the coil (resistance wire), it heats up and the heated coil then vaporizes the eliquid. 1 The bottom feed RBA is, perhaps, the easiest of all RBA types to build, maintain, and use. 2 It is filled from below, much like bottom coil clearomizer. 3 Bottom feed RBAs can utilize cotton instead of silica for the wick. 4 The Genesis, or genny, is a top feed RBA that utilizes a short woven mesh wire.", "Results-Based Accountability® (also known as RBA) is a disciplined way of thinking and taking action that communities can use to improve the lives of children, youth, families, adults and the community as a whole. RBA is also used by organizations to improve the performance of their programs. RBA improves the lives of children, families, and communities and the performance of programs because RBA: 1 Gets from talk to action quickly; 2 Is a simple, common sense process that everyone can understand; 3 Helps groups to surface and challenge assumptions that can be barriers to innovation;", "Results-Based Accountability® (also known as RBA) is a disciplined way of thinking and taking action that communities can use to improve the lives of children, youth, families, adults and the community as a whole. RBA is also used by organizations to improve the performance of their programs. Creating Community Impact with RBA. Community impact focuses on conditions of well-being for children, families and the community as a whole that a group of leaders is working collectively to improve. For example: “Residents with good jobs,” “Children ready for school,” or “A safe and clean neighborhood”.", "RBA uses a data-driven, decision-making process to help communities and organizations get beyond talking about problems to taking action to solve problems. It is a simple, common sense framework that everyone can understand. RBA starts with ends and works backward, towards means. The “end” or difference you are trying to make looks slightly different if you are working on a broad community level or are focusing on your specific program or organization. RBA improves the lives of children, families, and communities and the performance of programs because RBA: 1 Gets from talk to action quickly; 2 Is a simple, common sense process that everyone can understand; 3 Helps groups to surface and challenge assumptions that can be barriers to innovation;", "vs. NetIQ Identity Manager. Risk-based authentication (RBA) is a method of applying varying levels of stringency to authentication processes based on the likelihood that access to a given system could result in its being compromised. Risk-based authentication can be categorized as either user-dependent or transaction-dependent. User-dependent RBA processes employ the same authentication for every session initiated by a given user; the exact credentials that the site demands depend on who the user is.", "A rebuildable atomizer (RBA), often referred to as simply a “rebuildable,” is just a special type of atomizer used in the Vape Pen and Mod Industry that connects to a personal vaporizer. 1 The bottom feed RBA is, perhaps, the easiest of all RBA types to build, maintain, and use. 2 It is filled from below, much like bottom coil clearomizer. 3 Bottom feed RBAs can utilize cotton instead of silica for the wick. 4 The Genesis, or genny, is a top feed RBA that utilizes a short woven mesh wire.", "Get To Know Us. RBA is a digital and technology consultancy with roots in strategy, design and technology. Our team of specialists help progressive companies deliver modern digital experiences backed by proven technology engineering. " ]

    filtered_sentences = text_searcher.filter_sentences(sentences)
    filtered_sentences2 = [filtered_sentence for filtered_sentence in filtered_sentences if filtered_sentence[1]]
    print(filtered_sentences)

    sim = text_searcher.calculate_similarity(search_phrase,
                                             [filtered_sentence[2] for filtered_sentence in filtered_sentences])
    a = [((tup.item(),) + elem) for tup, elem in zip(sim, filtered_sentences2)]

    for b in a:
        print(b)