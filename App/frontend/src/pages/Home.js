import React, {useState} from 'react';
import axios from 'axios'
import "./Home.css"
import Loading from '../components/Loading';
const Home = (props) =>{
    
    const [logList, setLogList] = useState([])
    const [loading, setLoading] = useState(false)
    const onFileUpload = (event) =>{
        setLoading(true)
        const data = new FormData() 
        data.append('file', event.target.files[0])
        let url = "http://localhost:5005/crawl";
        axios.post(url, data)
        .then(res => { 
            setLoading(false)
            setLogList(res.data)
        }).catch(err=>{
            setLoading(false)
            alert(JSON.stringify(err, null, 2));
        })
    }    
    if(loading)
    return <Loading/>
    else
    return (<div>
        {logList.length > 0  && <table className="log-list-table">
            <thead >
                    <th  className="log-list-header log-header-bigger">
                        IP
                    </th>
                    <th  className="log-list-header log-header-bigger">
                        User agent
                    </th>
                    <th  className="log-list-header log-header-bigger">
                        MSE score
                    </th>
                    <th  className="log-list-header log-header-bigger">
                        Is crawler?
                    </th>
            </thead>
            <tbody> 
                {logList.map((listItem)=>{
                    return( 
                    <tr>
                        <td className="tr">
                            {listItem[0]}
                        </td>
                        <td className="tr">
                            {listItem[1]}
                        </td>
                        <td className="tr">
                            {listItem[2]}
                        </td>
                        <td className="tr">
                            {listItem[3]}
                        </td>
                    </tr> 
                    )
                })}

            </tbody>
        </table>}
        <label for="pic" className="upload-label">
            <span>Upload</span>
            <input type="file" name="file" id="pic" onChange={onFileUpload}/>
        </label>

    </div>)
}


export default Home